'''
Helper funations to be used.
'''

import math

def print_helper(properties, prop_text, units):
    '''
    Used to print out the properties
    '''
    dummy_i = 0
    print(' \n ')
    for prop_i in prop_text:
        print(str(prop_i) + ' ' + str(properties[dummy_i]) + ' ' + str(units[dummy_i]) )
        dummy_i += 1

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def get_num(x):
    try: return int(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
    except ValueError: return x

def list_2_string(list):
    new_string = ''
    for item in list[0:-1]:
        new_string += str(item)
        new_string += ' , '
    new_string += str(list[-1])
    return new_string

def one_load_combination(line_name_obj, coord, defined_loads, load_condition,
                         defined_tanks, comb_name, acc, load_factors_all):
    '''
    Creating load combination.
    Inserted into self.line_to_struc index = 4
    "dnva", "line12", "static_ballast_10m"
    #load combination dictionary (comb,line,load) : [stat - DoubleVar(), dyn - DoubleVar], on/off - IntVar()]
    :return:
    '''

    if load_condition not in ['tanktest','manual', 'slamming']:
        return helper_dnva_dnvb(line_name_obj, coord, defined_loads, load_condition,
                                defined_tanks, comb_name, acc, load_factors_all)
    elif load_condition ==  'tanktest' and comb_name == 'tanktest':
        return helper_tank_test(line_name_obj, coord, defined_loads, load_condition,
                                defined_tanks, comb_name, acc, load_factors_all)
    elif load_condition == 'manual':
        return helper_manual(line_name_obj, comb_name,load_factors_all)
    elif load_condition == 'slamming':
        return helper_slamming(defined_loads)
    else:
        return None

def helper_dnva_dnvb(line_name_obj, coord, defined_loads, load_condition,
                         defined_tanks, comb_name, acc, load_factors_all):

    # calculate the defined loads
    calc_load = []
    line_name = line_name_obj[0]
    structure_type = line_name_obj[1].get_structure_type()
    #print('---STRUCTURE TYPE---', structure_type)
    static_pressure,dynamic_pressure = 0,0
    #print('-----HELPER START FOR', comb_name, load_condition, line_name,'-----')
    if len(defined_loads) !=  0:
        for load in defined_loads :
            if load != None:
                #print('LOAD NAME: ',comb_name, line_name, load.get_name())
                load_factors = load_factors_all[(comb_name, line_name, load.get_name())]
                # USE GET() (static,dyn, on/off)
                if load_condition == load.get_load_condition():
                    static_pressure = (load_factors[2].get())*(load_factors[0].get())\
                                      *load.get_calculated_pressure(coord, acc[0],structure_type)
                    dynamic_pressure = (load_factors[2].get())*(load_factors[1].get())\
                                       *load.get_calculated_pressure(coord, acc[1],structure_type)
                    # print('load (NON-TANK) calculation for load condition:' , load_condition, ' - Load is: ', load.get_name(), ' - Type is: ')
                    # print('static with acc:', acc[0], ' is: ',str(load_factors[2].get()),'*',str(load_factors[0].get()),'*',
                    #      str(load.get_calculated_pressure(coord, acc[0],structure_type)), ' = ', static_pressure)
                    # print('dynamic with acc:', acc[1],' is: ',str(load_factors[2].get()),'*',str(load_factors[1].get()),'*',
                    #      str(load.get_calculated_pressure(coord, acc[1],structure_type)), ' = ', dynamic_pressure)
                    calc_load.append(static_pressure+dynamic_pressure)

    # calculate the tank loads

    if len(defined_tanks) != 0:
        temp_tank = {}

        for tank_name_obj in defined_tanks:
            temp_tank[tank_name_obj[0]] = 0

            load_factors = load_factors_all[(comb_name, line_name, tank_name_obj[0])]
            overpress_lf = [1.3,0]# if load_factors[0].get()==1.2 else [1,1.3]

            if load_condition == tank_name_obj[1].get_condition():
                # USE GET() (static,dyn, on/off)
                static_pressure = load_factors[2].get()*(load_factors[0].get())\
                                  *tank_name_obj[1].get_calculated_pressure(coord,acc[0])\
                                  +tank_name_obj[1].get_overpressure()*overpress_lf[0]
                dynamic_pressure = load_factors[2].get()*load_factors[1].get()\
                                   *tank_name_obj[1].get_calculated_pressure(coord,acc[1])\
                                   +tank_name_obj[1].get_overpressure()*overpress_lf[1]

                temp_tank[tank_name_obj[0]] = static_pressure + dynamic_pressure# .append((static_pressure + dynamic_pressure))
                # if line_name_obj[0] == 'line46':
                #     print('load (TANK) calculation for load condition:', load_condition, ' - Tank is: ', tank_name_obj[0])
                #     print('load factors : ', load_factors[0].get(),load_factors[1].get(),load_factors[2].get())
                #     print('static: ', str(load_factors[2].get()), '*', str(load_factors[0].get()) , '*',
                #           str(tank_name_obj[1].get_calculated_pressure(coord,acc[0])),' + ',
                #           str(tank_name_obj[1].get_overpressure()), '*',str(overpress_lf[0]), ' = ', static_pressure)
                #     print('dynamic: ',str(load_factors[2].get()), '*', str(load_factors[1].get()),  '*'
                #           ,str(tank_name_obj[1].get_calculated_pressure(coord, acc[1])),' + ',
                #           str(tank_name_obj[1].get_overpressure()), '*',str(overpress_lf[1]),' = ', dynamic_pressure)
            # choosing the tank with the highest pressures

        if len(defined_loads) == 0:
            line_tank_pressure_calc = max([pressure for pressure in temp_tank.values()])
            highest_dnv_tank_pressure  = tank_name_obj[1].get_tank_dnv_minimum_pressure(load_factors[0].get(),
                                                                                        load_factors[1].get())
            line_dnv_tank_pressure = tank_name_obj[1].get_line_pressure_from_max_pressure(highest_dnv_tank_pressure,
                                                                                          coord)

            # print('Tank load to append is max( ',highest_tank_pressure_calc,highest_dnv_tank_pressure,')')
            highest_tank_pressure = max(line_tank_pressure_calc,line_dnv_tank_pressure)
            calc_load.append(-highest_tank_pressure if highest_tank_pressure else 0)
        else:
            pass
    # print('-----HELPER END, RESULT IS: ', calc_load,'-----')

    return int(abs(sum(calc_load)))

def helper_slamming(defined_loads):

    # calculate the defined loads

    if len(defined_loads) != 0:
        for load in defined_loads:
            if load != None and load.get_load_condition() == 'slamming':
                return load.get_calculated_pressure(0, 0, 'slamming')


def helper_tank_test(line_name_obj, coord, defined_loads, load_condition,
                                defined_tanks, comb_name, acc, load_factors_all):
    # calculate the defined loads
    calc_load = []
    static_pressure, dynamic_pressure = 0, 0
    line_name = line_name_obj[0]
    structure_type = line_name_obj[1].get_structure_type()

    if len(defined_loads) != 0:
        for load in defined_loads:
            if load != None:
                load_factors = load_factors_all[(comb_name, line_name, load.get_name())]
                # USE GET() (static,dyn, on/off)
                if load_condition == load.get_load_condition():
                    static_pressure = (load_factors[2].get()) * (load_factors[0].get()) \
                                      * load.get_calculated_pressure(coord, acc[0], structure_type)
                    dynamic_pressure = (load_factors[2].get()) * (load_factors[1].get()) \
                                       * load.get_calculated_pressure(coord, acc[1], structure_type)
                    calc_load.append(static_pressure + dynamic_pressure)

    # calculate the tank loads
    temp_tank={}
    if len(defined_tanks) != 0:

        for tank_name_obj in defined_tanks:
            temp_tank[tank_name_obj[0]] = []

        for tank_name_obj in defined_tanks:
            load_factors = load_factors_all[(comb_name, line_name, tank_name_obj[0])]
            # print('tank test LF: ', load_factors[0],load_factors[1],load_factors[2])
                # USE GET() (static,dyn, on/off)
            overpress_lf = [1.3, 0] if load_factors[0].get() == 1.2 else [1, 0]
            static_pressure = (load_factors[2].get()) * (load_factors[0].get())\
                              * tank_name_obj[1].get_calculated_pressure(coord, acc[0])\
                              +tank_name_obj[1].get_overpressure()*overpress_lf[0]
            dynamic_pressure = (load_factors[2].get()) * (load_factors[1].get())\
                               * tank_name_obj[1].get_calculated_pressure(coord, acc[1])\
                               +tank_name_obj[1].get_overpressure()*overpress_lf[1]

            temp_tank[tank_name_obj[0]].append((static_pressure + dynamic_pressure))
        # choosing the tank with the highest pressures
        if len(defined_tanks) != 0:
            highest_tank_pressure = max([temp_tank[tank[0]] for tank in defined_tanks])
            calc_load.append(-highest_tank_pressure[0] if len(highest_tank_pressure) > 0 else 0)
        else:
            pass
    return int(abs(sum(calc_load)))

def helper_manual(line_name, comb_name,load_factors_all):

    load_factors = load_factors_all[(comb_name, line_name[0], 'manual')]

    return load_factors[0].get() * load_factors[1].get() * load_factors[2].get()

