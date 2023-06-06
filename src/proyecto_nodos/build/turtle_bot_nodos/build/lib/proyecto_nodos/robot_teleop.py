#! /usr/bin/env python

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from pynput import keyboard as kb
from proyecto_interfaces.srv import StartNavigationTest

class teleop(Node):
    """Crea objetos de tipo nodo."""
    
    def __init__(self):
        """Constructor de la clase teleop."""

        super().__init__("turtle_bot_teleop")

        self.cmd_publisher = self.create_publisher(Twist,'/turtlebot_cmdVel',10)
        self.srv = self.create_service(StartNavigationTest, "/group_11/start_navigation_test_srv", self.autonomous_navigation)

        self.linear_vel = 200.0
        self.angular_vel = 100.0

        self.get_logger().info("Turtle Teleop has been started correctly.")

    def autonomous_navigation(self,request,response):
        self.x = request.x
        self.y = request.y

        response.answer = "se aprobo el servicio"
        return response

    def key_callback(self,a,l):
        """Multiplica la velocidad lineal y angular por -1 o 1 dependiendo de la tecla presionada. Publica el
        mensaje tipo Twist en el tópico '/turtlebot_cmdVel'."""

        twist_mss = Twist()
        twist_mss.linear.x = a*self.linear_vel #a=1 adelante
        twist_mss.angular.z = l*self.angular_vel #l=1 derecha
        self.cmd_publisher.publish(twist_mss)

    def on_press(self,key):
        """Cuando se presiona una tecla en el teclado, si es 'w','a','s' o 'd' asigna un valor a las variables
        a y l que multiplican por 1 o -1 las velocidades lineales y angulares respectivamente.
        
        Args:
            key: tecla presionada en el teclado
        """
        try:
            if key.char in ['w','a','s','d']:
                a = 0
                l = 0
                if key.char == 'w':
                    a = 1
                elif key.char =='s':
                    a = -1
                elif key.char == 'd':
                    l = -1
                else:
                    l = 1
                self.key_callback(a,l)
            else:
                print("[INFO] La tecla presionada no tiene un movimiento asociado \n Siga las instrucciones.")
        except:
            print("Caracter especial no identificado.")
        
    def on_release(self,key):
        """Cuando se deja de presionar la tecla, llama a la función que detiene el movimiento del robot.
        Publica en el tópico '/turtlebot_route' el String que contiene la tecla presionada y el tiempo que
        se presionó.
        
        Args:
            key: tecla que se dejo de presionar en el teclado.
        """
        twist_mss = Twist()
        twist_mss.linear.x = 0.0
        twist_mss.angular.z = 0.0
        self.cmd_publisher.publish(twist_mss)
        
    def listen_keyboard(self):
        """Ecucha el teclado y esta a la espera de que se presione una tecla para ejecutar alguna función."""
        with kb.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()

def main(args=None):
    rclpy.init(args=args)
    teleop_node = teleop()
    
    teleop_node.listen_keyboard()
    rclpy.spin(teleop_node)
    
    teleop.destroy_node()
    rclpy.shutdown()
    
if __name__== "__main__":
    main()