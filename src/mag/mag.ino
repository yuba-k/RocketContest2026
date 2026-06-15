#include <Wire.h>
#include <LIS3MDL.h>
#define N 100//キャリブレーションのデータ取得回数

LIS3MDL mag;
char report[80];
float x_tmp[N], y_tmp[N];//キャリブレーション用仮データ記憶変数
float x_offset = 0.0;
float y_offset = 0.0;

void calibrate(){
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
    delay(100);
  }
  for(int i = 0; i < N; i++){
    x_max = max(x_max, x_tmp[i]);
    y_max = max(y_max, y_tmp[i]);
    x_min = min(x_min, x_tmp[i]);
    y_min = min(y_min, y_tmp[i]);
  }
  x_offset = (x_max+x_min)/2.0;
  y_offset = (y_max+y_min)/2.0;
  digitalWrite(13, LOW);
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
  calibrate();
}

void loop() {
  mag.read();
  snprintf(report, sizeof(report), "x:%d,y:%d,z:%d",(int)(mag.m.x-x_offset),(int)(mag.m.y-y_offset),mag.m.z);
  Serial.println(report);
  delay(100);
}
