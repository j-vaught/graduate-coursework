clc;
clear;
format compact;
x=1;
y=2;
z=3;

a=2;
b=3;
c=4;

Vector1 =[x,y,z];
Vector2 =[a,b,c];

Magnitude1=sqrt(Vector1(1)^2+Vector1(2)^2+Vector1(3)^2);
Magnitude2=sqrt(Vector2(1)^2+Vector2(2)^2+Vector2(3)^2);

unitVector1=Vector1/Magnitude1;
unitVector2=Vector2/Magnitude2;
Dot=dot(Vector1, Vector2);
AngleBetween2Vectors=acos(Dot/(Magnitude1*Magnitude2))*180/pi;

Cross=cross(Vector1, Vector2);
