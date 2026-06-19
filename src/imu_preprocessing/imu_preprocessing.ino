// """
// 9軸センサ制御プログラム
// """
#include <Wire.h>
#include <LIS3MDL.h>
#include <LSM6.h>
#include <MadgwickAHRS.h>
#define N 100//キャリブレーションのデータ取得回数
#define PI 3.141593
#define DT 0.1//[s]

LIS3MDL mag;
LSM6 imu;
Madgwick filter;

char report[80];
float x_tmp[N], y_tmp[N];//キャリブレーション用仮データ記憶変数
//地磁気のオフセット
float m_x_offset = 0.0;
float m_y_offset = 0.0;
float m_z_offset = 0.0;
//ジャイロのオフセット
float g_x_offset = 0.0;
float g_y_offset = 0.0;
float g_z_offset = 0.0;

void gyro_calib(){
  int x_sum = 0;
  int y_sum = 0;
  int z_sum = 0;
  digitalWrite(13, HIGH);
  for(int i = 0; i < N; i++){
    imu.read();
    x_sum += imu.g.x;
    y_sum += imu.g.y;
    z_sum += imu.g.z;
    delay(DT*1000);
  }
  digitalWrite(13, LOW);
  g_x_offset = x_sum/N;
  g_y_offset = y_sum/N;
  g_z_offset = z_sum/N;
}

void hard_iron(){
  //水平面(x,y)のハードアイアン補正
  //10Hz
  int x_max = -32768;
  int y_max = -32768;
  int x_min = 32767;
  int y_min = 32767;
  digitalWrite(13, HIGH);
  for(int i = 0; i < N; i++){
    mag.read();
    x_tmp[i] = mag.m.x;
    y_tmp[i] = mag.m.y;
    delay(DT*1000);
  }
  for(int i = 0; i < N; i++){
    x_max = max(x_max, x_tmp[i]);
    y_max = max(y_max, y_tmp[i]);
    x_min = min(x_min, x_tmp[i]);
    y_min = min(y_min, y_tmp[i]);
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
  filter.begin(1/DT);
}

void loop() {
  mag.read();
  imu.read();
  int x_mg = mag.m.x - m_x_offset;
  int y_mg = mag.m.y - m_y_offset;
  int z_mg = mag.m.z;
  int degree = atan2(y_mg,x_mg)*(180/PI);
  int x_g = imu.g.x - g_x_offset;
  int y_g = imu.g.y - g_y_offset;
  int z_g = imu.g.z - g_z_offset;

  //snprintf(report, sizeof(report), "x:%d,y:%d,z:%d,θ:%d\n%d,%d,%d",(int)x_mg,(int)y_mg,mag.m.z,degree,x_g,y_g,z_g);
  filter.update(x_g, y_g, z_g, imu.a.x, imu.a.y, imu.a.z, x_mg, y_mg, z_mg);
  Serial.print("ROLL:");
  Serial.print(filter.getRoll(), 2);

  Serial.print(",PITCH:");
  Serial.print(filter.getPitch(), 2);

  Serial.print(",YAW:");
  Serial.println(filter.getYaw(), 2);
  delay(DT*1000);
}
