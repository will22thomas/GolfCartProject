import lcm
import time
import dpkt
import cv2
import os
import numpy as np
import open3d as o3d

from datetime import datetime
from ouster import client
from lidar_package import item
from contextlib import closing
from more_itertools import time_limited
import matplotlib.pyplot as plt
    

# streaming live data by sampling
def sample_live_data(hostname):
    msg = item()

    msg.x2Coordinate = [3.0, 5.0, 7.0, 9.0]
    msg.y2Coordinate = [3.0, 5.0, 7.0, 9.0]
    msg.z2Coordinate = [3.0, 5.0, 7.0, 9.0]

    msg.timestamp = "date month year"
    msg.framecount = 0

    show = True
    lc = lcm.LCM()
    while show:
        metadata, sample = client.Scans.sample(hostname, 1, 7502)
        scan = next(sample)[0]

        # transform data to 3d points
        xyzlut = client.XYZLut(metadata)
        xyz = xyzlut(scan.field(client.ChanField.RANGE))

        [x, y, z] = [c.flatten() for c in np.dsplit(xyz, 3)]

        msg.x2Coordinate = x
        msg.y2Coordinate = y
        msg.z2Coordinate = z
        # key = cv2.waitKey(1) & 0xFF
        # if key == 27: # esc key
        #     show = False
        #     break

        time_part = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        msg.timestamp = time_part
        msg.framecount += 1
        
        # publish data
        lc.publish("DATA", msg.encode())

# Streaming live data by streaming
def stream_live_data(hostname, lidar_port):
    msg = item()

    msg.x2Coordinate = [3.0, 5.0, 7.0, 9.0]
    msg.y2Coordinate = [3.0, 5.0, 7.0, 9.0]
    msg.z2Coordinate = [3.0, 5.0, 7.0, 9.0]

    msg.timestamp = "date month year"
    msg.framecount = 0

    lc = lcm.LCM()
    with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
        for scan in stream:
            # xyz_something = client.destagger(stream.metadata, scan.field(client.ChanField.RANGE))
            xyzlut = client.XYZLut(stream.metadata)
            xyz = xyzlut(scan.field(client.ChanField.RANGE))
            [x, y, z] = [c.flatten() for c in np.dsplit(xyz, 3)]

            msg.x2Coordinate = x
            msg.y2Coordinate = y
            msg.z2Coordinate = z

            # print("This is x: ", x)
            # print("This is y: ", y)
            # print("This is z: ", z)

            time_part = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            msg.timestamp = time_part
            msg.framecount += 1
        
            # publish data
            lc.publish("DATA", msg.encode())

def plot_data_sample(hostname, port):
    import matplotlib.pyplot as plt  # type: ignore

    # get single scan
    metadata, sample = client.Scans.sample(hostname, 1, port)
    scan = next(sample)[0]

    # set up figure
    plt.figure()
    ax = plt.axes(projection='3d')
    r = 3
    ax.set_xlim3d([-r, r])
    ax.set_ylim3d([-r, r])
    ax.set_zlim3d([-r, r])

    plt.title("3D Points from {}".format(hostname))

    xyzlut = client.XYZLut(metadata)
    xyz = xyzlut(scan.field(client.ChanField.RANGE))

    [x, y, z] = [c.flatten() for c in np.dsplit(xyz, 3)]
    ax.scatter(x, y, z, c=z / max(z), s=0.2)
    plt.show()

def live_plot_reflectivity(hostname: str, lidar_port: int = 7502) -> None:
    import cv2

    print("press ESC from visualization to exit")
    with closing(client.Scans.stream(hostname, lidar_port,
                                     complete=False)) as stream:
        show = True
        while show:
            for scan in stream:
                reflectivity = client.destagger(stream.metadata,
                                          scan.field(client.ChanField.REFLECTIVITY))
                reflectivity = (reflectivity / np.max(reflectivity) * 255).astype(np.uint8)
                cv2.imshow("scaled reflectivity", reflectivity)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    show = False
                    break
        cv2.destroyAllWindows()

def stream_data_make_pcd(hostname, lidar_port):
    msg = item()

    msg.x2Coordinate = [3.0, 5.0, 7.0, 9.0]
    msg.y2Coordinate = [3.0, 5.0, 7.0, 9.0]
    msg.z2Coordinate = [3.0, 5.0, 7.0, 9.0]

    msg.timestamp = "date month year"
    msg.framecount = 0

    pcap_to_pcd()
    #TODO: work around here

    lc = lcm.LCM()
    with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
        for scan in stream:
            xyzlut = client.XYZLut(stream.metadata)

            xyz = xyzlut(scan.field(client.ChanField.RANGE))
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(xyz.reshape(-1,3))

            reflectivity = client.destagger(stream.metadata,
                                          scan.field(client.ChanField.REFLECTIVITY))
            reflectivity = (reflectivity / np.max(reflectivity) * 255).astype(np.uint8)

            print("This is reflectivity: ", reflectivity)

            x = 3
            y = 4
            z = 5
            msg.x2Coordinate = x
            msg.y2Coordinate = y
            msg.z2Coordinate = z

            print("This is x: ", x)
            print("This is y: ", y)
            print("This is z: ", z)

            # print("This is pcd: ", np.asarray(pcd.points))

            time_part = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            msg.timestamp = time_part
            msg.framecount += 1
        
            # publish data
            lc.publish("DATA", msg.encode())


#             float x, y, z;
#             int intensity;
#             vector<vector<float>> xyzVector;
#             vector<int64_t> intensityVector;
#             // Get the x,y,z, and intensity values from each line
#             for(int i = 0; i < points; i++){
#               getline(infile, line);
#               int pos = line.find(" ");
#               x = stof(line.substr(0, pos));
#               line.erase(0, pos+1);
#               pos = line.find(" ");
#               y = stof(line.substr(0, pos));
#               line.erase(0, pos+1);
#               pos = line.find(" ");
#               z = stof(line.substr(0, pos));
#               line.erase(0, pos+1);
#               pos = line.find(" ");
#               intensity = stoi(line.substr(0, pos));
#               line.erase(0, pos+1);
#               // Add xyz to a 2D vector
#               vector<float> xyzRow { x, y, z };
#               xyzVector.push_back(xyzRow);
#               // Add intensity to a vector
#               intensityVector.push_back(intensity);
#             }
#             msg.coordinates = xyzVector;
#             msg.intensity = intensityVector;


def pcap_to_pcd(#source: client.PacketSource,
                #metadata: client.SensorInfo,
                hostname, lidar_port,
                num: int = 0,
                pcd_dir: str = ".",
                pcd_base: str = "pcd_out",
                pcd_ext: str = "pcd") -> None:
    "Write scans from a pcap to pcd files (one per lidar scan)."

    from itertools import islice

    if not os.path.exists(pcd_dir):
        os.makedirs(pcd_dir)

    with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
        for scan in stream:

            # precompute xyzlut to save computation in a loop
            xyzlut = client.XYZLut(stream.metadata)

    # create an iterator of LidarScans from pcap and bound it if num is specified
            # scans = iter(client.Scans(source))
            # if num:
            #     scans = islice(scans, num)

            for idx, scan in enumerate(scan):
                xyz = xyzlut(scan.field(client.ChanField.RANGE))
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(xyz.reshape(-1,3))
                pcd_path = os.path.join(pcd_dir, f'{pcd_base}_{idx:06d}.{pcd_ext}')
                print(f'write frame #{idx} to file: {pcd_path}')
                o3d.io.write_point_cloud(pcd_path, pcd)

def main():
    # stream_live_data("169.254.8.163", 7502)
    # plot_data_sample("169.254.8.163", 7502)
    live_plot_reflectivity("169.254.8.163")
    # sample_live_data("169.254.8.163")

    #stream_data_make_pcd("169.254.8.163", 7502)
    #pcap_to_pcd("169.254.8.163", 7502)

if __name__ == "__main__":
    main()