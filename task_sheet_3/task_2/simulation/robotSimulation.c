#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>

#define MAX_TIME 15000
#define PI 3.14159265359
#define SPEED 0.01
#define SENSOR_MAX_DIST 0.15

#define LAYERS 3
#define CONNECTIONS 8

#define NUM_RUNS 10  // Number of different configurations to test

float lightPosX;
float lightPosY;

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

void runSimulation(int runNumber, float x_init, float y_init, float heading_init) {
    FILE *logFile;
    char filename[100];
    float x, y, heading;
    int timeStep;
    float sensorLeft, sensorRight, sensorMid;
    float wheelLeft, wheelRight;
    float lightSensor;
    float accumulatedLight;
    
    // Create unique filename for this run
    sprintf(filename, "./run_logs/run_%03d.txt", runNumber);
    
    logFile = fopen(filename, "w");
    if(logFile == NULL) {
        printf("Error: Could not open log file %s\n", filename);
        return;
    }
    
    // Write header with initial configuration
    fprintf(logFile, "# Run %d: x_init=%.3f, y_init=%.3f, heading_init=%.3f, lightX=%.3f, lightY=%.3f\n",
            runNumber, x_init, y_init, heading_init, lightPosX, lightPosY);
    fprintf(logFile, "timeStep,x,y,heading,sensorLeft,sensorMid,sensorRight,lightSensor,wheelLeft,wheelRight\n");
    
    // Initialize robot position
    x = x_init;
    y = y_init;
    heading = heading_init;
    
    accumulatedLight = 0.0;
    
    // Run simulation
    for(timeStep=0; timeStep<MAX_TIME; timeStep++) {
        
        if(x>1.0) x=1.0;
        if(y>1.0) y=1.0;
        if(x<0.0) x=0.0;
        if(y<0.0) y=0.0;
        
        // Sensors
        sensorMid = raytrace(x, y, heading+0.0);
        sensorLeft = raytrace(x, y, heading+0.1*PI);
        sensorRight = raytrace(x, y, heading-0.1*PI);
        
        // Try to move
        x += SPEED * cos(heading);
        y += SPEED * sin(heading);
        
        // Hardware protection
        if( (sensorMid > 0.95) || (sensorLeft > 0.95) || (sensorRight > 0.95) ) {
            x -= SPEED * cos(heading);
            y -= SPEED * sin(heading);
        }
        
        // Light sensor
        lightSensor = (x-lightPosX)*(x-lightPosX)+(y-lightPosY)*(y-lightPosY);
        accumulatedLight += 2.0-lightSensor;
        
        // Neural network with noise
        propagate(sensorLeft + 0.02*(float)rand()/(float)RAND_MAX - 0.01,
                  sensorMid + 0.02*(float)rand()/(float)RAND_MAX - 0.01,
                  sensorRight + 0.02*(float)rand()/(float)RAND_MAX - 0.01,
                  lightSensor + 0.02*(float)rand()/(float)RAND_MAX - 0.01);
        wheelLeft = outLeft;
        wheelRight = outRight;
        
        // Update heading
        heading += (wheelLeft-wheelRight) * PI;
        
        // Log data
        fprintf(logFile, "%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                timeStep, x, y, heading, sensorLeft, sensorMid, sensorRight, 
                lightSensor, wheelLeft, wheelRight);
        
    } // for timeStep
    
    fclose(logFile);
    
    printf("Run %d completed: Start(%.2f,%.2f) Light(%.2f,%.2f) -> Final(%.2f,%.2f) Distance=%.3f\n",
           runNumber, x_init, y_init, lightPosX, lightPosY, x, y, sqrt(lightSensor));
}

int main(int argc, char **argv) {
    
    time_t *init_rand;
    FILE *f, *summaryFile;
    int j, k, runNum;
    int a, b;
    float x_init, y_init, heading_init;
    
    initObstacles();
    
    // Initialize random number generator
    init_rand = malloc(sizeof(time_t));
    srand(time(init_rand));
    free(init_rand);
    
    // Load network weights
    f = fopen("network", "r");
    if(f == NULL) {
        printf("Error: Could not open network file\n");
        return 1;
    }
    for(j=0; j<LAYERS; j++)
        for(k=0; k<CONNECTIONS; k++)
            fscanf(f, "%d %d %e", &a, &b, &weight[j][k]);
    fclose(f);
    
    // Create summary file
    summaryFile = fopen("runs_summary.txt", "w");
    fprintf(summaryFile, "run,x_init,y_init,heading_init,light_x,light_y\n");
    
    printf("Starting %d simulation runs with random configurations...\n\n", NUM_RUNS);
    
    // Run multiple simulations with different random configurations
    for(runNum = 1; runNum <= NUM_RUNS; runNum++) {
        
        // Random initial position (avoid edges, keep away from walls)
        x_init = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        y_init = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        heading_init = (float)rand()/(float)RAND_MAX * 2.0 * PI - PI;
        
        // Random light position (avoid edges)
        lightPosX = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        lightPosY = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        
        // Write to summary file
        fprintf(summaryFile, "%d,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                runNum, x_init, y_init, heading_init, lightPosX, lightPosY);
        
        // Run the simulation
        runSimulation(runNum, x_init, y_init, heading_init);
    }
    
    fclose(summaryFile);
    
    printf("\n=======================================================\n");
    printf("All %d simulations completed successfully!\n", NUM_RUNS);
    printf("Log files: robot_log_run_001.txt to robot_log_run_%03d.txt\n", NUM_RUNS);
    printf("Summary file: runs_summary.txt\n");
    printf("=======================================================\n");
    
    return 0;
}