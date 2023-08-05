

class CANifier {
public:

  void * m_handle;

  void _create1(int deviceNumber) {
    m_handle = c_CANifier_Create1(deviceNumber);
  }

  ~CANifier() {
    c_CANifier_Destroy(m_handle);
  }
  ctre::phoenix::ErrorCode _setLEDOutput(uint32_t dutyCycle, uint32_t ledChannel) {
    
    auto __ret = c_CANifier_SetLEDOutput(m_handle, dutyCycle, ledChannel );
    return __ret;
  }


  ctre::phoenix::ErrorCode setGeneralOutputs(uint32_t outputsBits, uint32_t isOutputBits) {
    
    auto __ret = c_CANifier_SetGeneralOutputs(m_handle, outputsBits, isOutputBits );
    return __ret;
  }


  ctre::phoenix::ErrorCode setGeneralOutput(uint32_t outputPin, bool outputValue, bool outputEnable) {
    
    auto __ret = c_CANifier_SetGeneralOutput(m_handle, outputPin, outputValue, outputEnable );
    return __ret;
  }


  ctre::phoenix::ErrorCode _setPWMOutput(uint32_t pwmChannel, uint32_t dutyCycle) {
    
    auto __ret = c_CANifier_SetPWMOutput(m_handle, pwmChannel, dutyCycle );
    return __ret;
  }


  ctre::phoenix::ErrorCode _enablePWMOutput(uint32_t pwmChannel, bool bEnable) {
    
    auto __ret = c_CANifier_EnablePWMOutput(m_handle, pwmChannel, bEnable );
    return __ret;
  }


  bool getGeneralInput(uint32_t inputPin) {
    bool measuredInput;
     c_CANifier_GetGeneralInput(m_handle, inputPin, &measuredInput );
    return measuredInput;
  }


  std::array<double, 2> getPWMInput(uint32_t pwmChannel) {
    std::array<double, 2> dutyCycleAndPeriod;
     c_CANifier_GetPWMInput(m_handle, pwmChannel, dutyCycleAndPeriod.data() );
    return dutyCycleAndPeriod;
  }


  ctre::phoenix::ErrorCode getLastError() {
    
    auto __ret = c_CANifier_GetLastError(m_handle );
    return __ret;
  }


  double getBusVoltage() {
    double batteryVoltage;
     c_CANifier_GetBusVoltage(m_handle, &batteryVoltage );
    return batteryVoltage;
  }


  int getQuadraturePosition() {
    int pos;
     c_CANifier_GetQuadraturePosition(m_handle, &pos );
    return pos;
  }


  ctre::phoenix::ErrorCode setQuadraturePosition(int pos, int timeoutMs) {
    
    auto __ret = c_CANifier_SetQuadraturePosition(m_handle, pos, timeoutMs );
    return __ret;
  }


  int getQuadratureVelocity() {
    int vel;
     c_CANifier_GetQuadratureVelocity(m_handle, &vel );
    return vel;
  }


  std::tuple<int, int> getQuadratureSensor() {
    int pos;int vel;
     c_CANifier_GetQuadratureSensor(m_handle, &pos, &vel );
    return std::make_tuple(pos,vel);
  }


  ctre::phoenix::ErrorCode configVelocityMeasurementPeriod(int period, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigVelocityMeasurementPeriod(m_handle, period, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configVelocityMeasurementWindow(int window, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigVelocityMeasurementWindow(m_handle, window, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClearPositionOnLimitF(bool clearPositionOnLimitF, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigClearPositionOnLimitF(m_handle, clearPositionOnLimitF, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClearPositionOnLimitR(bool clearPositionOnLimitR, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigClearPositionOnLimitR(m_handle, clearPositionOnLimitR, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configClearPositionOnQuadIdx(bool clearPositionOnQuadIdx, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigClearPositionOnQuadIdx(m_handle, clearPositionOnQuadIdx, timeoutMs );
    return __ret;
  }


  void setLastError(int error) {
    
     c_CANifier_SetLastError(m_handle, error );
    
  }


  ctre::phoenix::ErrorCode configSetParameter(int param, double value, uint8_t subValue, int ordinal, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigSetParameter(m_handle, param, value, subValue, ordinal, timeoutMs );
    return __ret;
  }


  double configGetParameter(int param, int ordinal, int timeoutMs) {
    double value;
     c_CANifier_ConfigGetParameter(m_handle, param, &value, ordinal, timeoutMs );
    return value;
  }


  std::tuple<int32_t, uint8_t> configGetParameter_6(int32_t param, int32_t valueToSend, int32_t ordinal, int32_t timeoutMs) {
    int32_t valueRecieved;uint8_t subValue;
     c_CANifier_ConfigGetParameter_6(m_handle, param, valueToSend, &valueRecieved, &subValue, ordinal, timeoutMs );
    return std::make_tuple(valueRecieved,subValue);
  }


  ctre::phoenix::ErrorCode configSetCustomParam(int newValue, int paramIndex, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigSetCustomParam(m_handle, newValue, paramIndex, timeoutMs );
    return __ret;
  }


  int configGetCustomParam(int paramIndex, int timoutMs) {
    int readValue;
     c_CANifier_ConfigGetCustomParam(m_handle, &readValue, paramIndex, timoutMs );
    return readValue;
  }


  ctre::phoenix::ErrorCode configFactoryDefault(int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigFactoryDefault(m_handle, timeoutMs );
    return __ret;
  }


  int _getFaults() {
    int param;
     c_CANifier_GetFaults(m_handle, &param );
    return param;
  }


  int _getStickyFaults() {
    int param;
     c_CANifier_GetStickyFaults(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode clearStickyFaults(int timeoutMs) {
    
    auto __ret = c_CANifier_ClearStickyFaults(m_handle, timeoutMs );
    return __ret;
  }


  int getFirmwareVersion() {
    int firmwareVers;
     c_CANifier_GetFirmwareVersion(m_handle, &firmwareVers );
    return firmwareVers;
  }


  bool hasResetOccurred() {
    bool hasReset;
     c_CANifier_HasResetOccurred(m_handle, &hasReset );
    return hasReset;
  }


  ctre::phoenix::ErrorCode setStatusFramePeriod(int frame, uint8_t periodMs, int timeoutMs) {
    
    auto __ret = c_CANifier_SetStatusFramePeriod(m_handle, frame, periodMs, timeoutMs );
    return __ret;
  }


  int getStatusFramePeriod(int frame, int timeoutMs) {
    int periodMs;
     c_CANifier_GetStatusFramePeriod(m_handle, frame, &periodMs, timeoutMs );
    return periodMs;
  }


  ctre::phoenix::ErrorCode setControlFramePeriod(int frame, int periodMs) {
    
    auto __ret = c_CANifier_SetControlFramePeriod(m_handle, frame, periodMs );
    return __ret;
  }


};