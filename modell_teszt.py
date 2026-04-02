import random
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy import ScenarioObject

bng_home = r'C:\Program Files\BeamNG\BeamNG.tech.v0.38.3.0'
bng = BeamNGpy('localhost', 64256, home=bng_home)
bng.open()

scenario_name = f'fizika_teszt_{random.randint(1, 99999)}'
scenario = Scenario('smallgrid', scenario_name)

vehicle = Vehicle('ego_vehicle', model='etk800', license='PROJEKT2')

#road_model = ScenarioObject(
#    oid='custom_road_mesh',
#    name='custom_road_mesh',
#    otype='TSStatic',
#    pos=(0.0, 0.0, 0.03),     
#    rot_quat=(0.0, 0.0, 0.0, 1.0), # rot_quat-ot használunk, tizedestörtekkel!
#    scale=(1.0, 1.0, 1.0),
#    shapeName='/levels/smallgrid/art/shapes/a/sceneDirFinalTest.dae', 
#
#    collisionType='Visible Mesh',
#    decalType='None'
#    ##decalType='Visible Mesh'
#    ##complexCollision='1'
#)
#scenario.add_object(road_model)

pothole_visual = ScenarioObject(
    oid='latvany_modell',
    name='latvany_modell',
    otype='TSStatic',
    pos=(0.0, -10.0, 0.0),     
    rot_quat=(0.0, 0.0, 0.0, 1.0),
    scale=(1.0, 1.0, 1.0),
    shapeName='/levels/smallgrid/art/shapes/a/scaneView.dae',

    collisionType='None',  
    decalType='None'
)
scenario.add_object(pothole_visual)

pothole_physics = ScenarioObject(
    oid='fizika_modell',
    name='fizika_modell',
    otype='TSStatic',
    pos=(0.0, -10.0, 0.0),     
    rot_quat=(0.0, 0.0, 0.0, 1.0),
    scale=(1.0, 1.0, 1.0),
    shapeName='/levels/smallgrid/art/shapes/a/scaneSimplifiedModelForPhysics.dae',

    collisionType='Visible Mesh',  
    decalType='None'
)
scenario.add_object(pothole_physics)

scenario.add_vehicle(vehicle, pos=(0, 0, 2.0), rot_quat=(0, 0, 0, 1))

print("Szimuláció generálása...")
scenario.make(bng)

print("Pálya betöltése...")
bng.scenario.load(scenario)

print("Start!")
bng.scenario.start()

input("Nyomj Entert a szimuláció bezárásához...")
bng.close()