# validated: 2018-07-20 DV 3a78cd307217 java/src/com/ctre/phoenix/motorcontrol/can/BaseMotorController.java
# ----------------------------------------------------------------------------
#  Software License Agreement
#
#  Copyright (C) Cross The Road Electronics.  All rights
#  reserved.
#
#  Cross The Road Electronics (CTRE) licenses to you the right to
#  use, publish, and distribute copies of CRF (Cross The Road) firmware files (*.crf) and Software
# API Libraries ONLY when in use with Cross The Road Electronics hardware products.
#
#  THE SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" WITHOUT
#  WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
#  LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
#  CROSS THE ROAD ELECTRONICS BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#  INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF
#  PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR SERVICES, ANY CLAIMS
#  BY THIRD PARTIES (INCLUDING BUT NOT LIMITED TO ANY DEFENSE
#  THEREOF), ANY CLAIMS FOR INDEMNITY OR CONTRIBUTION, OR OTHER
#  SIMILAR COSTS, WHETHER ASSERTED ON THE BASIS OF CONTRACT, TORT
#  (INCLUDING NEGLIGENCE), BREACH OF WARRANTY, OR OTHERWISE
# ----------------------------------------------------------------------------

import typing

from .sensorcollection import SensorCollection
from .btrajectorypoint import BTrajectoryPoint
from .trajectorypoint import TrajectoryPoint
from ._impl import (
    ControlMode,
    DemandType,
    ErrorCode,
    Faults,
    FollowerType,
    InvertType,
    LimitSwitchNormal,
    MotController,
    MotionProfileStatus,
    NeutralMode,
    ParamEnum,
    RemoteFeedbackDevice,
    RemoteLimitSwitchSource,
    RemoteSensorSource,
    StatusFrame,
    StickyFaults,
    VelocityMeasPeriod,
)


__all__ = ["BaseMotorController"]


class BaseMotorController(MotController):
    """Base motor controller features for all CTRE CAN motor controllers."""

    ControlMode = ControlMode
    DemandType = DemandType
    InvertType = InvertType
    LimitSwitchNormal = LimitSwitchNormal
    NeutralMode = NeutralMode
    ParamEnum = ParamEnum
    RemoteFeedbackDevice = RemoteFeedbackDevice
    RemoteLimitSwitchSource = RemoteLimitSwitchSource
    RemoteSensorSource = RemoteSensorSource
    StatusFrame = StatusFrame
    VelocityMeasPeriod = VelocityMeasPeriod

    def __init__(self, arbId: int) -> None:
        """
        Constructor for motor controllers.
        
        :param arbId:
        """
        super().__init__()

        self._create1(arbId)
        self.arbId = arbId
        self.sensorColl = SensorCollection(self)
        self.controlMode = ControlMode.PercentOutput

    def getDeviceID(self) -> int:
        """
        Returns the Device ID
        
        :returns: Device number.
        """
        return self.getDeviceNumber()

    __set4_modes = frozenset(
        {
            ControlMode.PercentOutput,
            # ControlMode.TimedPercentOutput,
            ControlMode.Velocity,
            ControlMode.Position,
            ControlMode.MotionMagic,
            # ControlMode.MotionMagicArc,
            ControlMode.MotionProfile,
            ControlMode.MotionProfileArc,
        }
    )

    def set(
        self,
        mode: ControlMode,
        demand0: float,
        demand1Type: DemandType = DemandType.Neutral,
        demand1: float = 0.0,
    ):
        """
        Sets the appropriate output on the talon, depending on the mode.

        :param mode:
            The output mode to apply.
        :param demand0:
            The output value to apply. such as advanced feed forward and/or auxiliary close-looping in firmware.

            In :attr:`.ControlMode.PercentOutput`, the output is between -1.0 and 1.0, with 0.0 as
            stopped.
            
            In :attr:`.ControlMode.Voltage` mode, output value is in volts.
            
            In :attr:`.ControlMode.Current` mode, output value is in amperes.
            
            In :attr:`.ControlMode.Speed` mode, output value is in position change / 100ms.
            
            In :attr:`.ControlMode.Position` mode, output value is in encoder ticks or an analog value, depending on the sensor.
            
            In :attr:`.ControlMode.Follower` mode, the output value is the integer device ID of the talon to duplicate.
        :param demand1Type:
            The demand type for demand1.
            
            * Neutral: Ignore demand1 and apply no change to the demand0 output.
            * AuxPID: Use demand1 to set the target for the auxiliary PID 1.
            * ArbitraryFeedForward: Use demand1 as an arbitrary additive value to the
              demand0 output.  In PercentOutput the demand0 output is the motor output,
              and in closed-loop modes the demand0 output is the output of PID0.
        :param demand1:
            Supplemental value.  This will also be control mode specific for future features.
    
        Arcade Drive Example::
        
            _talonLeft.set(ControlMode.PercentOutput, joyForward, DemandType.ArbitraryFeedForward, +joyTurn)
            _talonRght.set(ControlMode.PercentOutput, joyForward, DemandType.ArbitraryFeedForward, -joyTurn)
                    
        Drive Straight Example::
                            
            # Note: Selected Sensor Configuration is necessary for both PID0 and PID1.
            _talonLeft.follow(_talonRght, FollowerType.AuxOutput1)
            _talonRght.set(ControlMode.PercentOutput, joyForward, DemandType.AuxPID, desiredRobotHeading)
                            
        Drive Straight to a Distance Example::
        
            # Note: Other configurations (sensor selection, PID gains, etc.) need to be set.
            _talonLeft.follow(_talonRght, FollowerType.AuxOutput1);
            _talonRght.set(ControlMode.MotionMagic, targetDistance, DemandType.AuxPID, desiredRobotHeading)
        
        """
        self.controlMode = mode

        if mode in self.__set4_modes:
            self._set_4(mode, demand0, demand1, demand1Type)
        elif mode is ControlMode.Follower:
            # did caller specify device ID
            if 0 <= demand0 <= 62:
                work = self.getBaseID()
                work >>= 16
                work <<= 8
                work |= int(demand0) & 0xFF
            else:
                work = int(demand0)
            self._set_4(mode, work, demand1, demand1Type)
        elif mode is ControlMode.Current:
            self.setDemand(mode, int(1000.0 * demand0), 0)  # milliamps
        else:
            self.setDemand(mode, 0, 0)

    def neutralOutput(self):
        """Neutral the motor output by setting control mode to disabled."""
        self.set(ControlMode.Disabled, 0, 0)

    def setInverted(self, invert: typing.Union[bool, InvertType]):
        """
        Inverts the hbridge output of the motor controller.

        This does not impact sensor phase and should not be used to correct sensor polarity.

        This will invert the hbridge output but NOT the LEDs.
        This ensures....

        - Green LEDs always represents positive request from robot-controller/closed-looping mode.
        - Green LEDs correlates to forward limit switch.
        - Green LEDs correlates to forward soft limit.
        
        :param invert:
            Invert state to set.
        """
        self.invert = int(invert)
        super()._setInverted_2(self.invert)

    def getInverted(self) -> bool:
        """:returns: invert setting of motor output"""
        if self.invert in (0, 1):
            return bool(self.invert)
        return super().getInverted()

    def getMotorOutputVoltage(self) -> float:
        """:returns: applied voltage to motor in volts"""
        return self.getBusVoltage() * self.getMotorOutputPercent()

    def getMotionProfileStatus(self) -> MotionProfileStatus:
        """
        Retrieve all status information.
        For best performance, Caller can snapshot all status information regarding the
        motion profile executer.
        """
        return MotionProfileStatus(*self._getMotionProfileStatus_2())

    def pushMotionProfileTrajectory(
        self, trajPt: typing.Union[TrajectoryPoint, BTrajectoryPoint]
    ) -> ErrorCode:
        """Push another trajectory point into the top level buffer (which is emptied
        into the motor controller's bottom buffer as room allows).

        :param trajPt: New point to push into buffer. You can use either the
                       :class:`.BTrajectoryPoint` or the legacy :class:`.TrajectoryPoint`
                       tuples. See the documentation for those structures for
                       details of the contents of each point.
        
        :returns: CTR_OKAY if trajectory point push ok. ErrorCode if buffer is
            full due to kMotionProfileTopBufferCapacity.
        
        .. note:: This function works on a real robot, but has not yet
                  been implemented in simulation mode. See :ref:`api_support`
                  for more details.
        """
        if len(trajPt) == 8:
            return self._pushMotionProfileTrajectory_2(*trajPt)
        else:
            return self._pushMotionProfileTrajectory_3(*trajPt)

    def getFaults(self) -> Faults:
        """Gets the last error generated by this object.

        Not all functions return an error code but can potentially report errors.
        This function can be used to retrieve those error codes.
        """
        return Faults(self._getFaults())

    def getStickyFaults(self) -> StickyFaults:
        """
        Polls the various sticky fault flags.
        """
        return StickyFaults(self._getStickyFaults())

    def getBaseID(self) -> int:
        return self.arbId

    def follow(
        self,
        masterToFollow: "BaseMotorController",
        followerType: FollowerType = FollowerType.PercentOutput,
    ):
        """
        Set the control mode and output value so that this motor controller will
        follow another motor controller. Currently supports following Victor SPX
        and Talon SRX.
        """
        id32 = masterToFollow.getBaseID()
        id24 = id32
        id24 >>= 16
        id24 = id24 & 0xFFFF
        id24 <<= 8
        id24 |= id32 & 0xFF

        if followerType == FollowerType.PercentOutput:
            self.set(ControlMode.Follower, id24)
        elif followerType == FollowerType.AuxOutput1:
            # follow the motor controller, but set the aux flag
            # to ensure we follow the processed output
            self.set(ControlMode.Follower, id24, DemandType.AuxPID, 0)
        else:
            self.neutralOutput()

    def valueUpdated(self):
        """
        When master makes a device, this routine is called to signal the update."""
        pass

    def getSensorCollection(self) -> SensorCollection:
        """
        :returns: object that can get/set individual raw sensor values."""
        return self.sensorColl

    def getControlMode(self) -> ControlMode:
        """
        :returns: control mode motor controller is in"""
        return self.controlMode

    def configAuxPIDPolarity(self, invert: bool, timeoutMs: int) -> ErrorCode:
        """Configures the Polarity of the Auxiliary PID (PID1).
        
        Standard Polarity:
        
        * Primary Output = PID0 + PID1
        * Auxiliary Output = PID0 - PID1
        
        Inverted Polarity:
        
        * Primary Output = PID0 - PID1
        * Auxiliary Output = PID0 + PID1
        
        :param invert:    If true, use inverted PID1 output polarity.
        
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for config
                          success and report an error if it times out. If zero, no
                          blocking or checking is performed.
        
        :returns: Error Code
        """
        return self.configSetParameter(
            ParamEnum.ePIDLoopPolarity, 1 if invert else 0, 0, 1, timeoutMs
        )
