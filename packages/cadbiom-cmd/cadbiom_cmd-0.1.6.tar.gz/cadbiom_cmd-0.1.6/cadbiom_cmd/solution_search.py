# -*- coding: utf-8 -*-
# Copyright (C) 2017  IRISA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
"""
Search Minimal Accessibility Conditions
"""
from __future__ import unicode_literals
from __future__ import print_function

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

# Standard imports
import os
from functools import partial
import sys
import itertools as it
# Multiprocessing
try:
    from concurrent.futures import ProcessPoolExecutor, as_completed
except ImportError:
    raise ImportError("No module named concurrent.futures. \
                      You can try to install 'futures' module in Python 2.7")
import multiprocessing as mp

# Custom imports
from cadbiom.models.clause_constraints.mcl.MCLAnalyser import MCLAnalyser
from cadbiom.models.clause_constraints.mcl.MCLQuery import MCLSimpleQuery
import cadbiom.commons as cm

LOGGER = cm.logger()


class ErrorRep(object):
    """Cf class CompilReporter(object):
    gt_gui/utils/reporter.py
    """
    def __init__(self):
        self.context = ""
        self.error = False

    def display(self, mess):
        self.error = True
        LOGGER.error(">> Context: %s; %s", self.context, mess)
        exit()

    def display_info(self, mess):
        LOGGER.error("-- Context: %s; %s", self.context, mess)
        exit()

    def set_context(self, cont):
        self.context = cont


def logical_operator(elements, operator):
    """Join elements with the given logical operator.

    :param arg1: Iterable of elements to join with a logical operator
    :param arg2: Logical operator to use 'and' or 'or'
    :return: logical_formula: str - AND/OR of the input list
    :type arg1: <list>
    :type arg2: <str>
    :rtype: <str>
    """
    assert operator in ('and', 'or')
#    print(operator + ": elements:", elements)

    return '(' + " {} ".format(operator).join(elements) + ')'


def make_logical_formula(previous_frontier_places, start_prop):
    """Make a logical formula based on previous results of MAC.

    The aim is to exclude previous solution.

    - 1 line: ``"A B" => (A and B)``
    - another line: ``"B C" => (B and C)``
    - merge all lines: ``(A and B) or (B and C)``
    - forbid all combinaisons: ``not((A and B) or (B and C))``

    :param arg1: Set of previous frontier places (previous solutions).
    :param arg2: Original property (constraint) for the solver.
    :return: A logical formula which excludes all the previous solutions.
    :type arg1: <set>
    :type arg2: <str>
    :rtype: <str>
    """

    logical_and = partial(logical_operator, operator='and')
    logical_or = partial(logical_operator, operator='or')

    def add_start_prop(prev_frontier_places_formula):
        """Deal with start_prop if given"""

        if start_prop and prev_frontier_places_formula:
            return start_prop + ' and (' + prev_frontier_places_formula + ')'
        elif prev_frontier_places_formula:
            return prev_frontier_places_formula
        return start_prop

    mac_list = [logical_and(frontier_places)
                for frontier_places in previous_frontier_places]

    if mac_list:
        # Logical or between each line
        return add_start_prop('not(' + logical_or(mac_list) + ')')
    return add_start_prop('')


def main2(chart_file, mac_file, mac_step_file, mac_complete_file, mac_strong_file,
          steps, final_prop, start_prop, inv_prop, all_macs, continue_run, limit):
    """

    :param chart_file: Model file (bcx, xml, cal).
    :param mac_file: File used to store Minimal Activation Condition (MAC/CAM).
    :param mac_step_file: File used to store Minimal step numbers for each solution.
    :param mac_complete_file: File used to store MAC & trajectories.
    :param mac_strong_file: ???
    :param steps: Maximal steps to reach the solutions.
    :param final_prop: Formula: Property that the solver looks for.
    :param start_prop: Formula: Original property (constraint) for the solver.
    :param inv_prop: Formula: ???
    :param all_macs: If set to True (not default), search all macs with
        less or equal steps than previous, by limiting steps.
    :param continue_run: If set to True (not default), previous macs from a previous
        run, will be reloaded.
    :param limit: Limit the number of solutions.
    :type chart_file: <str>
    :type mac_file: <str>
    :type mac_step_file: <str>
    :type mac_complete_file: <str>
    :type mac_strong_file: <str>
    :type steps: <int>
    :type final_prop: <str>
    :type start_prop: <str>
    :type inv_prop: <str>
    :type all_macs: <boolean>
    :type continue_run: <boolean>
    :type limit: <int>

    .. todo: handle these QUERY PARAMETERS... from GUI program

            #    if self.possible:
            #        if len(inv_prop) == 0:
            #            inv_prop = None
            #        else :
            #            inv_prop = "not ("+inv_prop+")"
            #    else:
            #        if len(inv_prop) != 0:
            # sert pas:
            #            final_prop = "not ("+final_prop+" and "+inv_prop+")"
    """


    # Build MCLA with Error Reporter
    mcla = MCLAnalyser(ErrorRep())

    # Load model file
    detect_model_type(mcla, chart_file)(chart_file)
    if mcla.reporter.error:
        raise "Error during loading of file"


    # Frontier places asked
    if continue_run:
        # Reload previous working files
        try:
            previous_frontier_places = read_mac_file(mac_file)
            current_start_prop = make_logical_formula(previous_frontier_places,
                                                      start_prop)
            LOGGER.info("%s:: Reload previous frontier places: %s",
                        final_prop,
                        len(previous_frontier_places))
        except IOError:
            LOGGER.warning("%s:: mac file not found!", final_prop)
            previous_frontier_places = set()
            current_start_prop = start_prop
    else:
        # New run
        previous_frontier_places = set()
        current_start_prop = start_prop


    i = len(previous_frontier_places)-1 if previous_frontier_places else 0
    #with PyCallGraph(output=GraphvizOutput()):
    while True:
        print("START PROP:", current_start_prop)

        # EXIT
        i += 1
        if i >= limit:
            LOGGER.info("%s:: Reaching the limitation of the number of solutions!",
                        final_prop)
            return

        ret = \
            find_mac(mcla,
                     mac_file, mac_step_file, mac_complete_file,
                     steps, final_prop, current_start_prop, inv_prop)

        if ret:
            frontier_places, min_steps = ret
        else:
            # No new solution/not satisfiable
            return

        # Add theese frontier places to set of previous ones
        # (tuple is hashable)
        previous_frontier_places.add(tuple(frontier_places))
        LOGGER.debug("%s:: Prev frontier places: %s",
                     final_prop,
                     previous_frontier_places)

        # Compute the formula of the next start_property
        current_start_prop = make_logical_formula(previous_frontier_places,
                                                  start_prop)

        # If all_macs flag is not set (to True),
        # search allways macs with less or equal steps than previous,
        # by limiting steps.
        # If all_macs == True: The limit is always the maximal number given
        # in 'step' setting.
        if not all_macs:
            steps = min_steps

        LOGGER.debug("%s:: Next start_prop formula: %s in %s steps",
                     final_prop,
                     current_start_prop,
                     steps)


def find_macs(mcla,
              mac_file, mac_step_file, mac_complete_file,
              steps, final_prop, start_prop, inv_prop):
    """__mac_exhaustive_search, on cherche d´abord des solutions non minimales
    (lfsol = self.__sq_dimacs_frontier_solutions(query, nb_step, 2))
    pour ensuite les élaguer en supprimer les places non essentielles à la
    satisfiabilité de la propriété
    (current_mac = self.__prune_frontier_solution(small_sol, query, nb_step)).
    Ce processus récursif est le plus "time-consuming" car nous n´avons pas
    le control sur les solutions fournies par SAT et les solutions non minimale
    sont en générales tres éloignées de la solution minimale,
    cad contiennent beaucoup plus de places.

    :return: None
    """

    # Build query
    query = MCLSimpleQuery(start_prop, inv_prop, final_prop)

    vmac_list = mcla.mac_search(query, steps)

    # If yes, in how many steps ?
    min_step = mcla.unfolder.get_current_step()
    for next_mac_object in vmac_list:

        LOGGER.debug("%s:: Next MAC object:\n%s", final_prop, next_mac_object)

        # Save MAC and timings
        LOGGER.debug("%s:: Save MAC and timings...", final_prop)
        with open(mac_complete_file, 'a') as file:
            next_mac_object.save(file)

        # Save MAC
        next_mac = next_mac_object.activated_frontier
        LOGGER.debug("%s:: Save next MAC: %s", final_prop, next_mac)
        with open(mac_file, 'a') as file:
            file.write('\t'.join(next_mac) + '\n')

    # Save min steps
    min_step = mcla.unfolder.get_current_step() - 1 # Magic number !
    LOGGER.debug("%s:: Save minimal steps: %s", final_prop, min_step)
    with open(mac_step_file, 'a') as file:
        file.write(str(min_step)+'\n')


def find_mac(mcla,
             mac_file, mac_step_file, mac_complete_file,
             steps, final_prop, start_prop, inv_prop):
    """
    list, min step

    :return: None if there is no new Solution or if problem is not satisfiable.
    """
    # Build query
    query = MCLSimpleQuery(start_prop, inv_prop, final_prop)

    # Is the property reacheable ?
    reacheable = mcla.sq_is_satisfiable(query, steps)
    # If yes, in how many steps ?
    min_step = mcla.unfolder.get_current_step()

    if reacheable and (min_step <= steps):
        LOGGER.info("%s:: Property %s is reacheable in %s steps",
                    final_prop, final_prop, min_step)
    else:
        LOGGER.info("%s:: Property %s is NOT reacheable in %s steps",
                    final_prop, final_prop, min_step)
        LOGGER.info("%s:: STOP the search!", final_prop)
        return

    # Find next MAC
    next_mac_object = mcla.next_mac(query, min_step)
    if next_mac_object:
        LOGGER.debug("%s:: Next MAC object:\n%s", final_prop, next_mac_object)

        # Save MAC and timings
        LOGGER.debug("%s:: Save MAC and timings...", final_prop)
        with open(mac_complete_file, 'a') as file:
            next_mac_object.save(file)

        # Save MAC (in alphabetic order...)
        next_mac = sorted(next_mac_object.activated_frontier)
        LOGGER.debug("%s:: Save next MAC: %s", final_prop, next_mac)
        with open(mac_file, 'a') as file:
            file.write(" ".join(sorted(next_mac, key=lambda s: s.lower()))+'\n')

        # Save min steps
        min_step = mcla.unfolder.get_current_step() - 1 # Magic number !
        LOGGER.debug("%s:: Save minimal steps: %s", final_prop, min_step)
        with open(mac_step_file, 'a') as file:
            file.write(str(min_step)+'\n')

        return next_mac, min_step

    LOGGER.info("%s:: STOP the search! No more MAC.", final_prop)


def detect_model_type(mclanalyser, filepath):
    """Return the function to use to load the model.

    The detection is based on the file extension.

    bcx file: Build an MCLAnalyser from a .bcx file:
        build_from_chart_file()
    cal file: Build an MCLAnalyser from a .cal file of PID database
        build_from_cadlang()
    xml file: Build an MCLAnalyser from a .xml file of PID database:
        build_from_pid_file()

    :param arg1: MCLAnalyser.
    :param arg2: File that contains the model.
    :type arg1: <MCLAnalyser>
    :type arg2: <str>
    :return: The function to use to read the given file.
    :rtype: <func>
    """

    build_func = {".bcx": mclanalyser.build_from_chart_file,
                  ".cal": mclanalyser.build_from_cadlang,
                  ".xml": mclanalyser.build_from_pid_file,
                 }

    _, extension = os.path.splitext(filepath)
    LOGGER.debug("Found %s extension: %s", extension, filepath)

    if extension not in build_func:
        LOGGER.error("Unauthorized file: %s", filepath)
        exit()

    return build_func[extension]


#def main(chart_file, mac_file, mac_step_file, mac_complete_file, mac_strong_file,
#         steps, final_prop, start_prop, inv_prop, all_macs):
#
#    LOGGER.debug("Params: start: {}, inv: {}, final: {}".format(start_prop,
#                                                                inv_prop,
#                                                                final_prop))
#
#    mac_p = None
#    # forbid previous mac
#    try :
#        mac_p = camFile2notOr(mac_file)
#        print("mac file:", mac_p)
#    except :
#        print('error in camFile2notOr')
#
#    if start_prop and mac_p :
#        start_prop += ' and ('+mac_p+')'
#    elif mac_p :
#        start_prop = mac_p
#
#    # BUILD MCLA
#    error_reporter = ErrorRep()
#    mcla = MCLAnalyser(error_reporter)
#    mcla.build_from_chart_file(chart_file)
#
#    if error_reporter.error:
#        #cancel_warn(error_reporter.memory)
#        #error_reporter.reset()
#        #return
#        print("ERROR:: " + error_reporter.error)
#        raise
##
#    # BUILD QUERY
#    query = MCLSimpleQuery(start_prop, inv_prop, final_prop)
#
#    # Frontier init:
#    # on_yn function:
#    # reach = self.mcla.sq_is_satisfiable(query, max_step)
#
#    # Show solutions:
#    #on_cond function:
##    lsol = mcla.sq_frontier_solutions(query, step, 10)
##    print("DEBUG:: " + str(lsol))
##    print("DEBUG:: ", len( lsol))
#
#    # minimal activation conditions
#    # on_mac function:
##    mac_list = self.mcla.mac_search(query, self.max_step)
##            if len(mac_list)==0 :
##                ok_warn("The solver returns an empty list" +
##                        "\n"+" you should refine your query")
#
#    # OPTIMIZE STEP RESEARCH
#    if os.path.isfile(mac_step_file):
#        min_step = int(get_last_line(mac_step_file))
#        print("min_step opti:", min_step)
#        query.set_steps_before_reach(min_step-1)
#
#
#    reacheable = mcla.sq_is_satisfiable(query, steps) #important step
#    print("reacheable:", reacheable)
#    min_step = mcla.unfolder.get_current_step()
#    print("min_step:", min_step)
#    # Set max step authorized
#    query.set_steps_before_reach(min_step-1)
#
#    # FIND NEXT MAC
#    next_mac_object = mcla.next_mac(query, min_step) #important step
#    print("next_mac_object:", next_mac_object)
#    if next_mac_object:
#
#        # SAVE MAC AND TIMING
#        with open(mac_complete_file, 'a') as file:
#            next_mac_object.save(file)
#
#        # SAVE MAC
#        next_mac = next_mac_object.activated_frontier
#        print("save next mac:", next_mac)
#        write_list(next_mac, mac_file)
#
#        # SAVE STEP
#        min_step = mcla.unfolder.get_current_step()
#        print("save min step:", min_step)
#        with open(mac_step_file, 'a') as file:
#            file.write(str(min_step)+'\n')
#
#        return 0
#    else:
#        print("stop")
#        return 1


def compute_combinations(final_properties):
    """Return all combinations of final properties.

    .. note:: (in case of input_file and combinations set).

    :param: List of final properties.
    :type: <list>
    :return: List of str. Each str is a combination of final_properties linked
        by a logical 'and'.

        :Example:

            ``('TGFB1', 'COL1A1'), ('TGFB1', 'decorin')``
            gives: ``['TGFB1 and COL1A1', 'TGFB1 and decorin']``

    :rtype: <list <str>>
    """

    final_properties = set(final_properties)

    def get_formula(data):
        """Include all elements in the combinations and exclude explicitely,
        all other elements.
        """

        negated_places = ' and not '.join(final_properties - data)
        return "{}{}{}".format(
            ' and '.join(data),
            ' and not ' if negated_places != '' else '',
            negated_places
        )


    all_combinations = list()
    for i in range(1, len(final_properties) + 1):

        all_combinations.append(
            {get_formula(set(comb)) for comb in it.combinations(final_properties, i)}
        )

    # Unpack combinations
    all_combinations = [comb for comb in it.chain(*all_combinations)]
    LOGGER.debug("Combinations: %s, Length: %s", all_combinations, all_combinations)
    LOGGER.info("Number of computed combinations: %s", len(all_combinations))

    return all_combinations


def solutions_search(params):
    """Launch the search for Minimum Activation Conditions (MAC) for entities
    of interest.

    * If there is no input file, there will be only one process.
    * If an input file is given, there will be 1 process per line
      (per logical formula on each line).
    """

#    params = args_to_param(args)

    # No input file
    if params['final_prop']:
        compute_macs(params)

    else:
        # Multiple properties in input file
        # => multiprocessing: 1 process for each property

        with open(params['input_file'], 'r') as f_d:
            g = (line.rstrip('\n') for line in f_d)

            final_properties = [prop for prop in g if prop != '']

        if params['combinations']:
            # If input_file is set, we can compute all combinations of
            # final_properties. default: False
            final_properties = compute_combinations(final_properties)

        LOGGER.debug("Final properties: %s", final_properties)
        # Output combinations of final_properties
#        with open(params['input_file'] + '_combinations.txt', 'w') as f_d:
#            f_d.write('\n'.join(final_properties) + '\n')
#
#        g = (elem for elem in final_properties)
#        for i in range(1, len(final_properties) + 1):
#            with open(params['input_file'][:-4] + '_combinations' + str(i) + '.txt', 'w') as f_d:
#                try:
#                    f_d.write(next(g) + '\n')
#                    f_d.write(next(g) + '\n')
#                except StopIteration:
#                    break
#
#        exit()

        def update_params(prop):
            """Shallow copy of parameters and update final_prop for a new run"""
            new_params = params.copy()
            new_params['final_prop'] = prop
            return new_params

        # Fix number of processes
        # PS: the new solver is optimized for 8 threads
#        nb_cpu_required = mp.cpu_count() / 8
#        nb_cpu_required = 1 if nb_cpu_required == 0 else nb_cpu_required

        with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:

            futures_and_output = {executor.submit(compute_macs,
                                                  update_params(job_property)
                                                 ):job_property \
                                for job_property in final_properties} # Job name

        nb_errors = 0
        nb_done = 0
        for future in as_completed(futures_and_output):

            job_name = futures_and_output[future]

            # On affiche les résultats si les futures en contiennent.
            # Si elles contiennent une exception, on affiche l'exception.
            if future.exception() is not None:
                LOGGER.error("%s generated an exception: \n%s",
                             job_name,
                             future.exception())
                nb_errors += 1
            else:
                # The end
                LOGGER.info("%s... \t\t[Done]", job_name)
                nb_done += 1

        LOGGER.info("Ending: %s errors, %s done\nbye.", nb_errors, nb_done)


def compute_macs(params):
    """Launch Cadbiom search of MACs (Minimal Activation Conditions).

    This function is called 1 or multiple times according to the necessity
    to use multiprocessing (Cf launch_researchs()).

    .. note:: Previous result files will be deleted.

    """

    # Limit recursion
    sys.setrecursionlimit(10000)

    # QUERY PARAMETERS
    model_filename = os.path.basename(os.path.splitext(params['chart_file'])[0])

    # FILES
    # Add trailing '/' if not present
    output = params['output'] if params['output'][-1] == '/' \
                else params['output'] + '/'
    mac_file_prefix   = output + model_filename + \
                        '_' + params['final_prop'] + '_mac'
    # mac_file
    mac_file          = mac_file_prefix + ".txt"
    # mac_step_file
    mac_step_file     = mac_file_prefix + "_step.txt"
    # mac_complete_file
    mac_complete_file = mac_file_prefix + "_complete.txt"
    # mac_strong_file
    mac_strong_file   = mac_file_prefix + "_strongA.txt"

    def remove_file(file):
        """Reset files"""
        try:
            os.remove(file)
        except OSError:
            pass

    if not params['continue']:
        # Reset previous working files
        # PS: the reload is done in main2() function
        remove_file(mac_file)
        remove_file(mac_step_file)
        remove_file(mac_complete_file)
        remove_file(mac_strong_file)

    # MAC research
    main2(
        params['chart_file'],   # chart_file
        mac_file,               # mac_file
        mac_step_file,          # mac_step_file
        mac_complete_file,      # mac_complete_file
        mac_strong_file,        # mac_strong_file
        params['steps'], params['final_prop'],
        params['start_prop'], params['inv_prop'],
        params['all_macs'], params['continue'], params['limit'],
    )

def read_mac_file(file):
    """Return a list a fontier places already found in mac file

    .. note:: use make_logical_formula() to get the new start_prop of the run.

    :param: Mac file of a previous run
    :type: <str>
    :return: A set a frontier places.
    :rtype: <set>
    """

    with open(file, 'r') as f_d:
        return {tuple(line.rstrip('\n').split(' ')) for line in f_d}
