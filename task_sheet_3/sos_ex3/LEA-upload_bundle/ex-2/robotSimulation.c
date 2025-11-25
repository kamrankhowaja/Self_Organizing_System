#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include<string.h>

#define MAX_TIME 15000
#define PI 3.14159265359
#define SPEED 0.01
#define SENSOR_MAX_DIST 0.15

#define LAYERS 3
#define CONNECTIONS 8


#define RANDOM_INIT 0


float lightPosX = 0.8;
float lightPosY = 0.8;


char obstacles[1000][1000];
float weight[LAYERS][CONNECTIONS];
float outLeft;
float outRight;

float activation(float x) {
    return 2.0/(1.0+exp(-2.0*x))-1.0;
}


void propagate(float input0, float input1, float input2, float input3) {
    float hidden_net0, hidden_net1;
    float i_layer_0, i_layer_1, i_layer_2, i_layer_3;
    float netLeft, netRight;
    
    i_layer_0 = activation(input0*weight[0][0]);
    i_layer_1 = activation(input1*weight[0][1]);
    i_layer_2 = activation(input2*weight[0][2]);
    i_layer_3 = activation(input3*weight[0][3]);
    
    hidden_net0 = i_layer_0*weight[1][0] + i_layer_1*weight[1][1]
    + i_layer_2*weight[1][2] + i_layer_3*weight[1][3];
    hidden_net1 = i_layer_0*weight[1][4] + i_layer_1*weight[1][5]
    + i_layer_2*weight[1][6] + i_layer_3*weight[1][7];
    
    netLeft = activation(hidden_net0)*weight[2][0]
    + activation(hidden_net1)*weight[2][1];
    netRight = activation(hidden_net0)*weight[2][2]
    + activation(hidden_net1)*weight[2][3];
    
    outLeft = activation(netLeft);
    outRight = activation(netRight);
}

void initObstacles() {
    
    int i,j;
    
    for(i=0;i<1000;i++)
        for(j=0;j<1000;j++)
            obstacles[i][j]=0;
    
    for(i=0;i<1000;i++) {
        obstacles[0][i] = 1;
        obstacles[999][i] = 1;
        obstacles[1][i] = 1;
        obstacles[998][i] = 1;
        obstacles[2][i] = 1;
        obstacles[997][i] = 1;
    }
    for(i=0;i<1000;i++) {
        obstacles[i][0] = 1;
        obstacles[i][999] = 1;
        obstacles[i][1] = 1;
        obstacles[i][998] = 1;
        obstacles[i][2] = 1;
        obstacles[i][997] = 1;
    }
    
    for(i=0;i<300;i++) {
        obstacles[i][399] = 1;
        obstacles[i][398] = 1;
        obstacles[i][397] = 1;
    }
    for(i=700;i<1000;i++) {
        obstacles[i][599] = 1;
        obstacles[i][598] = 1;
        obstacles[i][597] = 1;
    }
    for(i=0;i<800;i++) {
        obstacles[500][i] = 1;
        obstacles[501][i] = 1;
        obstacles[502][i] = 1;
    }
}


float raytrace(float xStart, float yStart, float dir) {
    float dist = 0.0;
    float x = xStart, y = yStart;
    
    while(1) {
        if(obstacles[(int)(x*1000.0)][(int)(y*1000.0)])
            return (SENSOR_MAX_DIST - dist)/SENSOR_MAX_DIST;
        else {
            x += 0.00015 * cos(dir);
            y += 0.00015 * sin(dir);
            if( (x>1.0) || (x<0.0) || (y>1.0) || (y<0.0) )
                return (SENSOR_MAX_DIST - dist)/SENSOR_MAX_DIST;
            dist += 0.00015;
        }
        if(dist > SENSOR_MAX_DIST)
            return 0.0;
    }
}




int main(int argc, char **argv) {
    
    time_t *init_rand;
    FILE *f;
    float x,y,heading;
    int timeStep, i, j, k;
    float sensorLeft, sensorRight, sensorMid;
    float wheelLeft, wheelRight;
    float turningCostSum;
    float sensorActivation;
    float lightSensor;
    float accumulatedLight;
    
    initObstacles();
    
    /* init random number generator */
    init_rand = malloc(sizeof(time_t));
    srand(time(init_rand));
    free(init_rand);
    
    // load:
    int a, b;
    f = fopen("network", "r");
    for(j=0;j<LAYERS;j++)
        for(k=0;k<CONNECTIONS;k++)
            fscanf(f, "%d %d %e", &a, &b, &weight[j][k]);
    
    
    if(RANDOM_INIT) {
        x = (float)rand()/(float)RAND_MAX;
        y = (float)rand()/(float)RAND_MAX;
        heading = (float)rand()/(float)RAND_MAX * 2.0 * PI - PI;
    } else {
        x = 0.3;
        y = 0.8;
        heading = PI;
    }
    
    turningCostSum = 0.0;
    sensorActivation = 0.0;
    
    accumulatedLight = 0.0;
    
    for(timeStep=0;timeStep<MAX_TIME;timeStep++) {
        
        if(x>1.0)
            x=1.0;
        if(y>1.0)
            y=1.0;
        if(x<0.0)
            x=0.0;
        if(y<0.0)
            y=0.0;
        
        // sensors:
        sensorMid = raytrace(x,y,heading+0.0);
        sensorLeft = raytrace(x,y,heading+0.1*PI);
        sensorRight = raytrace(x,y,heading-0.1*PI);
        
        x += SPEED * cos(heading);
        y += SPEED * sin(heading);
        
        if( (sensorMid > 0.95) || (sensorLeft > 0.95) || (sensorRight > 0.95) ) {
            x -= SPEED * cos(heading);
            y -= SPEED * sin(heading);
        }
        
        
        lightSensor = (x-lightPosX)*(x-lightPosX)+(y-lightPosY)*(y-lightPosY);
        accumulatedLight += 2.0-lightSensor;
        
        propagate(sensorLeft + 0.02*(float)rand()/(float)RAND_MAX - 0.01,
                  sensorMid + 0.02*(float)rand()/(float)RAND_MAX - 0.01,
                  sensorRight + 0.02*(float)rand()/(float)RAND_MAX - 0.01,
                  lightSensor + 0.02*(float)rand()/(float)RAND_MAX - 0.01);
        wheelLeft = outLeft;
        wheelRight = outRight;
        
        heading += (wheelLeft-wheelRight) * PI;
        
    } // for timeStep
    
    return 0;
}
