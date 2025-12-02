#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>

#define MAX_TIME 15000
#define PI 3.14159265359
#define SPEED 0.01
#define SENSOR_MAX_DIST 0.15

#define NUM_RUNS 10

// FSM States
typedef enum {
    SEEK_LIGHT,
    AVOID_OBSTACLE,
    TURN_LEFT,
    TURN_RIGHT,
    WALL_FOLLOW_LEFT,
    WALL_FOLLOW_RIGHT
} RobotState;

float lightPosX;
float lightPosY;

char obstacles[1000][1000];

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

void computeMotorOutputs(RobotState state, float sensorLeft, float sensorMid, 
                         float sensorRight, float lightSensor, float x, float y,
                         float heading, float *wheelLeft, float *wheelRight) {
    
    // Compute angle to light
    float dx = lightPosX - x;
    float dy = lightPosY - y;
    float angleToLight = atan2(dy, dx);
    float headingError = angleToLight - heading;
    
    // Normalize angle to [-PI, PI]
    while(headingError > PI) headingError -= 2*PI;
    while(headingError < -PI) headingError += 2*PI;
    
    // State-based motor control
    switch(state) {
        case SEEK_LIGHT:
            // Move forward while steering toward light
            *wheelLeft = 0.7 + 0.3 * headingError / PI;
            *wheelRight = 0.7 - 0.3 * headingError / PI;
            
            // Reduce speed when close to light
            if(lightSensor < 0.05) {
                *wheelLeft *= 0.3;
                *wheelRight *= 0.3;
            }
            break;
            
        case AVOID_OBSTACLE:
            // Move backward
            *wheelLeft = -0.8;
            *wheelRight = -0.8;
            break;
            
        case TURN_LEFT:
            // Turn left in place
            *wheelLeft = -0.5;
            *wheelRight = 0.5;
            break;
            
        case TURN_RIGHT:
            // Turn right in place
            *wheelLeft = 0.5;
            *wheelRight = -0.5;
            break;
            
        case WALL_FOLLOW_LEFT:
            // Follow wall on left side
            *wheelLeft = 0.6;
            *wheelRight = 0.7;
            
            // Adjust based on left sensor
            if(sensorLeft > 0.5) {
                *wheelLeft = 0.8;
                *wheelRight = 0.5;
            } else if(sensorLeft < 0.2) {
                *wheelLeft = 0.5;
                *wheelRight = 0.8;
            }
            break;
            
        case WALL_FOLLOW_RIGHT:
            // Follow wall on right side
            *wheelLeft = 0.7;
            *wheelRight = 0.6;
            
            // Adjust based on right sensor
            if(sensorRight > 0.5) {
                *wheelLeft = 0.5;
                *wheelRight = 0.8;
            } else if(sensorRight < 0.2) {
                *wheelLeft = 0.8;
                *wheelRight = 0.5;
            }
            break;
    }
    
    // Clamp outputs to [-1, 1]
    if(*wheelLeft > 1.0) *wheelLeft = 1.0;
    if(*wheelLeft < -1.0) *wheelLeft = -1.0;
    if(*wheelRight > 1.0) *wheelRight = 1.0;
    if(*wheelRight < -1.0) *wheelRight = -1.0;
}

RobotState updateState(RobotState currentState, float sensorLeft, float sensorMid, 
                       float sensorRight, int *stateTimer) {
    
    (*stateTimer)++;
    
    // Hardware protection - immediate transition
    if(sensorMid > 0.95 || sensorLeft > 0.95 || sensorRight > 0.95) {
        *stateTimer = 0;
        return AVOID_OBSTACLE;
    }
    
    // State-specific transitions
    switch(currentState) {
        case SEEK_LIGHT:
            // Obstacle detected ahead
            if(sensorMid > 0.6) {
                *stateTimer = 0;
                return AVOID_OBSTACLE;
            }
            // Obstacle on left
            if(sensorLeft > 0.5 && sensorRight < 0.3) {
                *stateTimer = 0;
                return TURN_RIGHT;
            }
            // Obstacle on right
            if(sensorRight > 0.5 && sensorLeft < 0.3) {
                *stateTimer = 0;
                return TURN_LEFT;
            }
            // Wall following conditions
            if(sensorLeft > 0.3 && sensorLeft < 0.7) {
                *stateTimer = 0;
                return WALL_FOLLOW_LEFT;
            }
            if(sensorRight > 0.3 && sensorRight < 0.7) {
                *stateTimer = 0;
                return WALL_FOLLOW_RIGHT;
            }
            break;
            
        case AVOID_OBSTACLE:
            // Back away for a few steps
            if(*stateTimer > 10) {
                *stateTimer = 0;
                // Decide which way to turn
                if(sensorLeft > sensorRight) {
                    return TURN_RIGHT;
                } else {
                    return TURN_LEFT;
                }
            }
            break;
            
        case TURN_LEFT:
        case TURN_RIGHT:
            // Turn until obstacle cleared
            if(*stateTimer > 20 && sensorMid < 0.4) {
                *stateTimer = 0;
                return SEEK_LIGHT;
            }
            break;
            
        case WALL_FOLLOW_LEFT:
            // Exit wall following if wall lost or obstacle ahead
            if(sensorLeft < 0.15 || sensorMid > 0.6) {
                *stateTimer = 0;
                return SEEK_LIGHT;
            }
            break;
            
        case WALL_FOLLOW_RIGHT:
            // Exit wall following if wall lost or obstacle ahead
            if(sensorRight < 0.15 || sensorMid > 0.6) {
                *stateTimer = 0;
                return SEEK_LIGHT;
            }
            break;
    }
    
    return currentState;
}

const char* stateToString(RobotState state) {
    switch(state) {
        case SEEK_LIGHT: return "SEEK_LIGHT";
        case AVOID_OBSTACLE: return "AVOID_OBSTACLE";
        case TURN_LEFT: return "TURN_LEFT";
        case TURN_RIGHT: return "TURN_RIGHT";
        case WALL_FOLLOW_LEFT: return "WALL_FOLLOW_LEFT";
        case WALL_FOLLOW_RIGHT: return "WALL_FOLLOW_RIGHT";
        default: return "UNKNOWN";
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
    RobotState state = SEEK_LIGHT;
    int stateTimer = 0;
    
    sprintf(filename, "./run_logs_fsm/run_%03d.txt", runNumber);
    
    logFile = fopen(filename, "w");
    if(logFile == NULL) {
        printf("Error: Could not open log file %s\n", filename);
        return;
    }
    
    fprintf(logFile, "# Run %d: x_init=%.3f, y_init=%.3f, heading_init=%.3f, lightX=%.3f, lightY=%.3f\n",
            runNumber, x_init, y_init, heading_init, lightPosX, lightPosY);
    fprintf(logFile, "timeStep,x,y,heading,sensorLeft,sensorMid,sensorRight,lightSensor,wheelLeft,wheelRight,state\n");
    
    x = x_init;
    y = y_init;
    heading = heading_init;
    
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
        
        // Add noise to sensors
        float noisyLeft = sensorLeft + 0.02*(float)rand()/(float)RAND_MAX - 0.01;
        float noisyMid = sensorMid + 0.02*(float)rand()/(float)RAND_MAX - 0.01;
        float noisyRight = sensorRight + 0.02*(float)rand()/(float)RAND_MAX - 0.01;
        float noisyLight = lightSensor + 0.02*(float)rand()/(float)RAND_MAX - 0.01;
        
        // Update FSM state
        state = updateState(state, noisyLeft, noisyMid, noisyRight, &stateTimer);
        
        // Compute motor outputs based on state
        computeMotorOutputs(state, noisyLeft, noisyMid, noisyRight, noisyLight,
                           x, y, heading, &wheelLeft, &wheelRight);
        
        // Update heading
        heading += (wheelLeft - wheelRight) * PI;
        
        // Log data
        fprintf(logFile, "%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
                timeStep, x, y, heading, sensorLeft, sensorMid, sensorRight, 
                lightSensor, wheelLeft, wheelRight, stateToString(state));
        
    }
    
    fclose(logFile);
    
    printf("Run %d completed: Start(%.2f,%.2f) Light(%.2f,%.2f) -> Final(%.2f,%.2f) Distance=%.3f\n",
           runNumber, x_init, y_init, lightPosX, lightPosY, x, y, sqrt(lightSensor));
}

int main(int argc, char **argv) {
    
    time_t *init_rand;
    FILE *summaryFile;
    int runNum;
    float x_init, y_init, heading_init;
    
    initObstacles();
    
    init_rand = malloc(sizeof(time_t));
    srand(time(init_rand));
    free(init_rand);
    
    summaryFile = fopen("runs_summary_fsm.txt", "w");
    fprintf(summaryFile, "run,x_init,y_init,heading_init,light_x,light_y\n");
    
    printf("Starting %d FSM simulation runs with random configurations...\n\n", NUM_RUNS);
    
    for(runNum = 1; runNum <= NUM_RUNS; runNum++) {
        
        x_init = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        y_init = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        heading_init = (float)rand()/(float)RAND_MAX * 2.0 * PI - PI;
        
        lightPosX = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        lightPosY = 0.1 + (float)rand()/(float)RAND_MAX * 0.8;
        
        fprintf(summaryFile, "%d,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                runNum, x_init, y_init, heading_init, lightPosX, lightPosY);
        
        runSimulation(runNum, x_init, y_init, heading_init);
    }
    
    fclose(summaryFile);
    
    printf("\n=======================================================\n");
    printf("All %d FSM simulations completed successfully!\n", NUM_RUNS);
    printf("Log files: run_logs_fsm/run_001.txt to run_logs_fsm/run_%03d.txt\n", NUM_RUNS);
    printf("Summary file: runs_summary_fsm.txt\n");
    printf("=======================================================\n");
    
    return 0;
}