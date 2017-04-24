########################## Inputfile check ##########################
PRECI="";
if [ ${PRECISION} == "double" ];then
	PRECI="-dp"
fi
export LANG=en
######################### .pbs set ##########################
RANDOM_FILE=/tmp/$USER-ANSYS-`date +%Y%m%d%H%M%P%S`-$RANDOM
rm `find /tmp/$USER-ANSYS-* -user $USER` -rf
#rm /tmp/$USER-ANSYS-* -rf
cat << EOF > $RANDOM_FILE
#PBS -N ${JOB_NAME}
#PBS -l nodes=${NUM_NODES}:ppn=${PER_NODE} 
#PBS -l walltime=${TIMEMAX}
#PBS -j oe
#PBS -q ${QUEUE}
#PBS -m e
#PBS -M ${MAIL}
#PBS -d ${WORK_DIR}

NP=\`wc -l < \$PBS_NODEFILE\`
JOU_FILE=${INPUT_FILE}
LOG_FILE=${INPUT_FILE}.log

cd ${WORK_DIR}
np=1
for NODE in \`cat "\$PBS_NODEFILE"\`; do
   host=\$NODE
   if [ ! -z \$lasthost ]; then
     if [ \$host = \$lasthost ]; then
       np=\`expr \$np + 1\`
     else
       if [ -z \$mList ]; then
         mList=\$lasthost:\$np
       else
         mList=\$mList:\$lasthost:\$np
       fi
       np=1
     fi
   fi
   lasthost=\$host
done
cd ${WORK_DIR}
if [ -z \$mList ]; then
  mList=\$lasthost:\$np
else
  mList=\$mList:\$lasthost:\$np
fi

ansys121 -lsdynampp $PRECI -usessh -dis -machines \$mList i=${INPUT_FILE} > ${INPUT_FILE}.log
sleep 300
EOF

######################### Job sub ##########################
qsub $RANDOM_FILE

######################### Nothing ##########################
#if [[ $PORTALDEBUG -ne 1 ]];then
#rm $RANDOM_FILE -rf >& /dev/null
#fi
