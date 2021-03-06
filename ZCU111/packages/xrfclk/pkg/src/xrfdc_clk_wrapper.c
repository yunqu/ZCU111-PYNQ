#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include "xrfdc_clk.h"

#ifdef BOARD_ZCU111
int writeLmk04208Regs(int IicNum, unsigned int RegVals[26]) {
    unsigned int LMK04208_CKin[1][26];
    for(int i=0;i<26;i++)
	    LMK04208_CKin[0][i] = RegVals[i];
    LMK04208ClockConfig(IicNum, LMK04208_CKin);
    return 0;
 }
#endif /* BOARD_ZCU111 */
 
#ifdef BOARD_XUPRFSOC
int writeLmk04832Regs(int IicNum, unsigned int RegVals[125]) {
    unsigned int LMK04832_CKin[1][125];
    for(int i=0;i<125;i++)
	    LMK04832_CKin[0][i] = RegVals[i];
    LMK04832ClockConfig(IicNum, LMK04832_CKin);
    return 0;
}
#endif /* BOARD_XUPRFSOC */

#if defined(BOARD_XUPRFSOC) || defined(BOARD_ZCU111)
int writeLmx2594Regs(int IicNum, unsigned int RegVals[113]) {
    int XIicDevFile;
    char XIicDevFilename[20];

    sprintf(XIicDevFilename, "/dev/i2c-%d", IicNum);
    XIicDevFile = open(XIicDevFilename, O_RDWR);

    if (ioctl(XIicDevFile, I2C_SLAVE_FORCE, I2C_SPI_ADDR) < 0) {
      printf("Error: Could not set address \n");
      return 1;
    }

    Lmx2594Updatei2c(XIicDevFile, RegVals);
    close(XIicDevFile);
    return 0;
}

int clearInt(int IicNum){
    int XIicDevFile;
    char XIicDevFilename[20];

    sprintf(XIicDevFilename, "/dev/i2c-%d", IicNum);
    XIicDevFile = open(XIicDevFilename, O_RDWR);

    if (ioctl(XIicDevFile, I2C_SLAVE_FORCE, I2C_SPI_ADDR) < 0) {
      printf("Error: Could not set address \n");
      return 1;
    }

    SC18IS602ClearInt(XIicDevFile);
    close(XIicDevFile);
    return 0;
}
#endif /* BOARD_XUPRFSOC || BOARD_ZCU111 */

