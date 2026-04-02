import os
import time
import csv
import cv2
import random
import traceback
import numpy as np
from ultralytics import YOLO
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera
from beamngpy import ScenarioObject

bng_home = r'C:\Program Files\BeamNG\BeamNG.tech.v0.38.3.0'
beamng = BeamNGpy('localhost', 64251, home=bng_home)

save_dir = r'D:\Egyetem\6.felev\Szakdoga1\Implementacio\Saved_Detections'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

csv_path = os.path.join(save_dir, 'detections_log.csv')
if not os.path.exists(csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Kep_neve', 'Idopont', 'X', 'Y', 'Z', 'Conf'])

model = YOLO('D:/Egyetem/6.felev/Szakdoga1/Implementacio/FRDC_RDD/YOLOv10/weights/yolov10_x_best.pt')

scenario_name = f'pothole_pilot_{random.randint(1, 10000)}'
scenario = Scenario('automation_test_track', scenario_name)

vehicle = Vehicle('ego_vehicle', 'covet', license='PROJEKT2')

car_x = -294.787
car_y = -255.694
car_z = 118.813
scenario.add_vehicle(vehicle, pos=(car_x, car_y, car_z), rot_quat=(0.0, 0.0, -0.707, 0.707))

start_x = car_x + 5  
end_x = car_x + 30    

for i in range(5):
    pos_x = random.uniform(start_x, end_x)
    pos_y = random.uniform(car_y - 2.0, car_y + 2.0) 
    pos_z = car_z + 0.07

    pothole_visual = ScenarioObject(
        oid=f'latvany_modell_{i}',
        name=f'latvany_modell_{i}',
        otype='TSStatic',
        pos=(pos_x, pos_y, pos_z),
        rot_quat=(0.0, 0.0, 0.0, 1.0),
        scale=(1.0, 1.0, 1.0),
        shapeName= '/levels/automation_test_track/art/shapes/scaneView.dae',
        
        collisionType='None', 
        decalType='None'
    )
    scenario.add_object(pothole_visual)   

    pothole_physics = ScenarioObject(
        oid=f'fizika_modell_{i}',
        name=f'fizika_modell_{i}',
        otype='TSStatic',
        pos=(pos_x, pos_y, pos_z),
        rot_quat=(0.0, 0.0, 0.0, 1.0),
        scale=(1.0, 1.0, 1.0),
        shapeName= '/levels/automation_test_track/art/shapes/scaneSimplifiedModelForPhysics.dae',
        
        collisionType='Visible Mesh', 
        decalType='None'
    )
    scenario.add_object(pothole_physics)

img_counter = 0
last_save_time = 0

try:
    print("Csatlakozás és BeamNG indítása...")
    try: beamng.close() 
    except: pass

    beamng.open()
    scenario.make(beamng)
    beamng.scenario.load(scenario)
    beamng.scenario.start()

    print("Várakozás a rendszerre (5 mp)...")
    time.sleep(5)

    camera_1 = Camera('Camera 1', beamng, vehicle=vehicle, requested_update_time=0.05,
                  pos=(0.0, -0.477, 1.142), 
                  dir=(0, -1, 0), 
                  up=(0, 0, 1),
                  resolution=(1200, 600), 
                  field_of_view_y=70, 
                  near_far_planes=(0.05, 100), 
                  is_visualised=True)

    print("Detektálás indul! Nyomj 'q'-t a kilépéshez.")

    while True:
        try:
            sensor_data = camera_1.poll()
            
            if not sensor_data or 'colour' not in sensor_data:
                time.sleep(0.1)
                continue

            img_pil = sensor_data['colour'].convert('RGB')
            frame_rgb = np.array(img_pil)
            
            results = model.predict(frame_rgb, conf=0.35, verbose=False)
            
            if len(results[0].boxes) > 0:
                current_time = time.time()
                if current_time - last_save_time > 2.0:
                    vehicle.sensors.poll()
                    pos = vehicle.state['pos']
                    
                    annotated_frame = results[0].plot()
                    bgr_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
                    fname = f"katyu_{img_counter}.jpg"
                    cv2.imwrite(os.path.join(save_dir, fname), bgr_frame)
                    
                    with open(csv_path, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([fname, time.ctime(current_time), pos[0], pos[1], pos[2], f"{float(results[0].boxes.conf[0]):.2f}"])
                    
                    print(f"SZAKDOGA: Kátyú mentve ({fname}) - Pozíció: {pos[0]:.1f}, {pos[1]:.1f}")
                    img_counter += 1
                    last_save_time = current_time

            display_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            cv2.imshow('Kutatasi Monitor', display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as loop_e:
            print(f"Hiba az adatfogadásban: {loop_e}")
            time.sleep(1)
            continue
        
except Exception as main_e:
    print(f"\nVÁRATLAN HIBA TÖRTÉNT AZ INDÍTÁSKOR:\n")
    traceback.print_exc() 
finally:
    cv2.destroyAllWindows()
    try:
        beamng.close()
    except:
        pass