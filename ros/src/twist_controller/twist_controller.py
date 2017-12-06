"""
Definition of all classes used to compute values issued to control vehicle.
"""

import rospy

from yaw_controller import YawController
from twiddle import PIDWithTwiddle
from dbw_mkz_msgs.msg import BrakeCmd
from lpf_2stages import quick_lpf as lpf

GAS_DENSITY = 2.858
ONE_MPH = 0.44704

PRED_STEERING_FACTOR = 0.2
CORR_STEERING_FACTOR = 0.3


class Controller(object):
    """
    Controller encapsulates all logic to compute
    throttle, brake and steer commands.
    """

    def __init__(self,
                 vehicle_mass,
                 fuel_capacity,
                 brake_deadband,
                 decel_limit,
                 accel_limit,
                 wheel_radius,
                 wheel_base,
                 steer_ratio,
                 max_lat_accel,
                 max_steer_angle,
                 max_throttle_pct=1.0,
                 max_braking_pct=-1.0):

        self.brake_deadband = brake_deadband
        total_car_mass = vehicle_mass + fuel_capacity * GAS_DENSITY
        self.brake_car_factor = total_car_mass * wheel_radius
        self.decel_limit = decel_limit
        self.max_throttle_pct = max_throttle_pct
        self.max_braking_pct = max_braking_pct

        self.prev_time = rospy.get_time()
        self.avg_filter = lpf(nT1=2, nT2=15)
        self.avg_filter_brake = lpf(nT1=7, nT2=15)

        # twiddle algorithm is disabled so iterations and tolerance are here to show
        # what values to use when you want to activate twiddle.
        # current kp, ki and kd are values found from previous twiddle runs.
        self.steer_pid = PIDWithTwiddle("steering PID", kp=0.607900, ki=0.000172, kd=1.640951,
                                        mn=-max_steer_angle, mx=max_steer_angle,
                                        optimize_params=True, iterations=10, tolerance=0.05)
        self.accel_pid = PIDWithTwiddle("t/b PID", kp=1.806471, ki=0.00635, kd=0.715603,
                                        mn=decel_limit, mx=accel_limit,
                                        optimize_params=False, iterations=10, tolerance=0.05)

        self.max_steer_angle = max_steer_angle
        self.yaw_controller = YawController(wheel_base=wheel_base,
                                            steer_ratio=steer_ratio,
                                            min_speed=2.0,
                                            max_lat_accel=max_lat_accel,
                                            max_steer_angle=max_steer_angle)

    def control(self,
                dbw_enabled,
                cte,
                linear_velocity,
                angular_velocity,
                current_velocity):
        """

        Returns the values for throttle, brake and steer
        given current state of the car : ( CTE, current linear and angular velocity)
        and the desired linear velocity
        """

        throttle = 0.0
        brake = 0.0
        steer = 0.0

        if dbw_enabled:
            current_time = rospy.get_time()
            sample_time = current_time - self.prev_time
            self.prev_time = current_time

            predictive_steer = self.yaw_controller.get_steering(linear_velocity=linear_velocity,
                                                                angular_velocity=angular_velocity,
                                                                current_velocity=current_velocity)

            corrective_steer = self.steer_pid.step(
                error=cte, sample_time=sample_time)

            # steer = CORR_STEERING_FACTOR * corrective_steer + PRED_STEERING_FACTOR * predictive_steer
            steer = corrective_steer

            rospy.logdebug('steer = %f, cte = %f, corrective_steer = %f, predictive_steer = %f',
                           steer, cte, corrective_steer, predictive_steer)

            vel_delta = linear_velocity - current_velocity
            res_accel = self.accel_pid.step(error=vel_delta, sample_time=sample_time)

            res_accel = self.avg_filter.filter(res_accel)

            rospy.logdebug('desired vel = %f, current vel = %f, accel = %f',
                           linear_velocity, current_velocity, res_accel)

            if res_accel < 0.0 or linear_velocity < current_velocity:
                self.avg_filter.clear()
                if -res_accel < self.brake_deadband:
                    res_accel = 0.0

                throttle, brake = 0, self.avg_filter_brake.filter(BrakeCmd.TORQUE_MAX)*abs(self.max_braking_pct)
            else:
                if (res_accel > self.max_throttle_pct):
                    res_accel = self.max_throttle_pct
                throttle, brake = res_accel, 0

        else:
            self.steer_pid.reset()
            self.accel_pid.reset()
            self.prev_time = rospy.get_time()

        return throttle, brake, steer
