#!/bin/sh

#####################################################################################################################################################
#
#       Function Declarations
#
####################################################################################################################################################

retrieve_path() {
        echo "Retrieveing current working directory"
        Working_Directory=$(pwd)
}

run_ssd() {
        image_name=$1
        echo "Running SSD detection on" $image_name
        python SSD-Object-Detection.py --image-path=$image_name 
        
} 

run_YOLOv3() { 
        image_name=$1
        echo "Running YOLOv3 detection on" $image_name
        python recognition.py --image-path=$image_name  

}

run_YOLOv4() {
        image_name=$1
        echo "Running YOLOv4 detection on" $image_name

}

run_detection_sorting() {
        image_name=$1
        echo "Combining and reordering three model coordinates" $image_name
        python combiningFormat.py --path $image_name
}

run_ensemble_detection() {
        image_name=$1
        echo "Running ensemble_detection and RMSE calculation on" $image_name
        python ensembleMethod.py --path $image_name

}

######################################################################################################################################################
#
#       Main Function Body
#
######################################################################################################################################################

echo "Starting Ensemble Detection Method"
retrieve_path 

for file in $Working_Directory/inputs/*; 
        do
                echo "$(basename "$file")"
                run_YOLOv3 "$(basename "$file")"
                run_ssd "$(basename "$file")"
                run_detection_sorting "$(basename "$file")"
                #python SSD-Object-Detection.py --image-path="$(basename "$file")"
                #python recognition.py --image-path="$(basename "$file")"
                #python ensembleMethod.py --image-path="$(basename "$file")"
                #python combiningFormat.py --path "$(basename "$file")"
                run_ensemble_detection "$(basename "$file")" 
        done


