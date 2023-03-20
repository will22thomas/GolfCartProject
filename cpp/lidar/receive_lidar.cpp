#include <stdio.h>
#include <lcm/lcm-cpp.hpp>
#include "lidar_package/item.hpp"

class Handler 
{
    public:
        ~Handler() {}

        void handleMessage(const lcm::ReceiveBuffer* rbuf,
                const std::string& chan, 
                const lidar_package::item* msg)
        {
            int i;
            printf("Received message on channel \"%s\":\n", chan.c_str());
            printf("  timestamp   = %lld\n", msg->timestamp);
            printf("  framecount  = 5");
        }
};

int main(int argc, char** argv)
{
    lcm::LCM lcm;
    if(!lcm.good())
        return 1;

    Handler handlerObject;
    lcm.subscribe("EXAMPLE", &Handler::handleMessage, &handlerObject);

    while(0 == lcm.handle());

    return 0;
}