#include <lcm/lcm-cpp.hpp>
#include "lidar_package/item.hpp"
#include <iostream>
#include <chrono>

using namespace std;

// Creates an item object and fills it with the provided data.
// Returns the item object
lidar_package::item newItem(string timestamp, int64_t framecount, float coordinates, int64_t intensity)
{
    lidar_package::item item;
    item.timestamp = timestamp;
    item.framecount = framecount;
    item.coordinates = coordinates;
    item.intensity = intensity;
    return item;
}

// Simple program to publish hardcoded message data using LCM
// If the program is called without any command-line arguments it will publish a single item message
// If anything is present as a command-line argument, a status message with five items will be published instead
int main(int argc, char** argv)
{
    // Create LCM object and check that it was created successfully
    lcm::LCM lcm;
    if (!lcm.good())
    {
        std::cout << "LCM initialization failed" << std::endl;
        return 1;
    }
    // If no command line arguments are provided, run the program with a single item message,
    if (argc <= 1)
    {
        lidar_package::item msg;
        msg = newItem("Milk", 5, true);
        // Specifies the channel name for the message and publishes it
        lcm.publish("INDIVIDUAL", &msg);
    }
    // However, if any arguments are provided then run it with a hardcoded status message.
    else
    {
        std::string names[5] = {"Milk", "Cheese", "Ground Beef", "Salt", "Pepper"};
        int16_t costs[5] = {5, 30, 6, 1, 2};
        bool is_stocked[5] = {true, true, false, true, false};
        lidar_package::status msg;
        msg.timestamp = std::chrono::system_clock::now().time_since_epoch().count();
        msg.item_count = 5;
        for (int i = 0; i < 5; i++)
        {
            msg.items.push_back(newItem(names[i], costs[i], is_stocked[i]));
        }
        // Specifies the channel name for the message and publishes it
        lcm.publish("REPORT", &msg);
    }
    return 0;
}