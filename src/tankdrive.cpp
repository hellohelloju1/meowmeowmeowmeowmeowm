#include <iostream>
#include "main.h"
#define MOTOR_L1 11
#define MOTOR_L2 -12
#define MOTOR_R1 -13
#define MOTOR_R2 14
#define LIMIT_TOP -10
#define LIMIT_BOTTOMHAHA 30

void initialize() {
	pros::lcd::initialize();

}

void disabled() {}

void competition_initialize() {}

void autonomous() {}

void opcontrol() {

		while (true) {
			pros::MotorGroup MotorLeft ({MOTOR_L1, MOTOR_L2});
			pros::MotorGroup MotorRight ({MOTOR_R1, MOTOR_R2});
			pros::Controller master (pros::E_CONTROLLER_MASTER);
			float lefty = (float) master.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y) / 127 * 200;
			float rightx = (float) master.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X) / 127 * 200;
			pros::lcd::set_text(1, std::to_string(lefty));
			pros::lcd::set_text(2, std::to_string(rightx));
			if (lefty<LIMIT_TOP && LIMIT_BOTTOMHAHA<lefty) {
			MotorLeft.brake();
			MotorRight.brake();
			} else if (lefty>LIMIT_TOP){
			MotorLeft.move_velocity(lefty+rightx);
			MotorRight.move_velocity(lefty - rightx);
				
			} else {
			MotorLeft.move_velocity(lefty-rightx);
			MotorRight.move_velocity(lefty + rightx);
			}
   			pros::delay(20);
		}
}
//Bro fix all bugs in this code like rn

