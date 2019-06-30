# import spira.all as spira

# from spira.core.parameters.variables import *
# from spira.core.parameters.initializer import ParameterInitializer


# class SimulationParameters(ParameterInitializer):

#     def __set_parameters__(self, obj, **kwargs):
#         pass

#     def __init__(self, **kwargs):
#         pass


# class SimulationDefinition():
#     simul_params = DictParameter(doc='A set of simulation parameters.')


# class CellSimulationDefinition(SimulationDefinition):

#     def __init__(self, simul_params):
#         pass


# class __SimulationGeometry__(SimulationParameters):

#     cell = spira.CellParameter()
#     geometry = spira.Parameter(fdef_name='create_geometry')

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


# class CellSimulationGeometry(__SimulationGeometry__):

#     def create_geometry(self):
#         vp = virtual_process_model()
#         return vp.geometry


# def generate_simulation_geometry(cell, output=None):

#     simul_geom = CellSimulationGeometry()


