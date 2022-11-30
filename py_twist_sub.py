import rclpy
from rclpy.node import Node
from mp_msgs.msg import Hands
from std_msgs.msg import String

class MinimalSubscriber(Node):

    gestureInt = 0
    def __init__(self):
        super().__init__('handSub')
        self.subscription = self.create_subscription(Hands,'/hands',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        
        self.publisher = self.create_publisher(String, "/hands_gesture", 10)
        #self.timer = self.create_timer(0.5, self.timer_callback)
        

    # def timer_callback(self):

    #     msg = Int32()
    #     msg.data = gestureInt
    #     self.publisher_.publish(msg)

    
    def listener_callback(self, msg):
        gestureInt = 0


        handData = str(msg).split(", ")

        if len(handData) > 1:
            thumbTipX = handData[22][2:]
            thumbTipY = handData[23][2:]
            pointerMCPX = handData[27][2:]
            pointerMCPY = handData[28][2:]
            PointerKnuckleX = handData[32][2:]
            PointerKnuckleY = handData[33][2:]

           

            if float(pointerMCPY) - float(thumbTipY) > 75:
                print("THUMBS UP!")
                gestureInt = 1
            elif float(PointerKnuckleY) - float(thumbTipY) < -40:
                print("THUMBS DOWN!")
                gestureInt = 2
            elif float(thumbTipX) - float(pointerMCPX) > 35:
                print("THUMBS Left!")
                gestureInt = 3
            elif float(thumbTipX) - float(pointerMCPX) < -35:
                print("THUMBS Right!")
                gestureInt = 4
               
        msg = String()
       
        msg.data = str(gestureInt)
        self.publisher.publish(msg)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
