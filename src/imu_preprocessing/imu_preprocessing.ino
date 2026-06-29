// """
// 9軸センサ制御プログラム
// """
#include <Wire.h>
#include <LIS3MDL.h>
#include <LSM6.h>
#include <Adafruit_AHRS_Madgwick.h>
#define NG 100//ジャイロキャリブレーションのデータ取得回数
#define NMG 250//地磁気キャリブレーションのデータ取得回数
#define PI 3.141593
#define DT 0.02//[s]

LIS3MDL mag;
LSM6 imu;
Adafruit_Madgwick filter(0.3);


char report[80];
//地磁気のオフセット
float m_x_offset = 0.0;
float m_y_offset = 0.0;
float m_z_offset = 0.0;
//ジャイロのオフセット
float g_x_offset = 0.0;
float g_y_offset = 0.0;
float g_z_offset = 0.0;

unsigned long last;

void gyro_calib(){
  long x_sum = 0;
  long y_sum = 0;
  long z_sum = 0;
  digitalWrite(13, HIGH);
  for(int i = 0; i < NG; i++){
    imu.read();
    x_sum += imu.g.x;
    y_sum += imu.g.y;
    z_sum += imu.g.z;
    delay(DT*1000);
  }
  digitalWrite(13, LOW);
  g_x_offset = (float)x_sum/NG;
  g_y_offset = (float)y_sum/NG;
  g_z_offset = (float)z_sum/NG;
}

void hard_iron(){
  //水平面(x,y)のハードアイアン補正
  //10Hz
  int x_max = -32768;
  int y_max = -32768;
  int x_min = 32767;
  int y_min = 32767;
  digitalWrite(13, HIGH);
  for(int i = 0; i < NMG; i++){
    mag.read();
    x_max = max(x_max, mag.m.x);
    y_max = max(y_max, mag.m.y);
    x_min = min(x_min, mag.m.x);
    y_min = min(y_min, mag.m.y);
    delay(DT*1000);
  }
  m_x_offset = (x_max+x_min)/2.0;
  m_y_offset = (y_max+y_min)/2.0;
  digitalWrite(13, LOW);
}



void calibrate(){
  gyro_calib();
  delay(5000);
  hard_iron();
}

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  Wire.begin();
  if(!mag.init()){
    Serial.println("Failed to Detect");
    while(1);
  }
  mag.enableDefault();
  if(!imu.init()){
    Serial.println("Failed to Detect");
    while(1);
  }
  imu.enableDefault();
  calibrate();
  delay(2);
  for(int i = 0; i <= 10; i++){
    digitalWrite(13, HIGH);
    delay(300);
    digitalWrite(13, LOW);
  }
  last = micros();
}

void loop() {
  unsigned long now = micros();
  float dt = (now-last)*1e-6f;
  last = now;
  mag.read();
  imu.read();
  float x_mg = (mag.m.x - m_x_offset)/6842.0f;
  float y_mg = (mag.m.y - m_y_offset)/6842.0f;
  float z_mg = mag.m.z/6842.0f;
  float degree = atan2(y_mg,x_mg)*(180/PI);
  float x_g = (imu.g.x - g_x_offset)*8.75*0.001;
  float y_g = (imu.g.y - g_y_offset)*8.75*0.001;
  float z_g = (imu.g.z - g_z_offset)*8.75*0.001;
  float x_a = imu.a.x*0.061*0.001;
  float y_a = imu.a.y*0.061*0.001;
  float z_a = imu.a.z*0.061*0.001;
  filter.update(x_g, y_g, z_g, x_a, y_a, z_a, x_mg, y_mg, z_mg, dt);
  Serial.print("ROLL:");
  Serial.print(filter.getRoll(), 2);

  Serial.print(",PITCH:");
  Serial.print(filter.getPitch(), 2);

  Serial.print(",YAW:");
  Serial.print(filter.getYaw(), 2);
  Serial.print(",DEGREE:");
  Serial.println(degree);
  delay(DT*1000);
}
