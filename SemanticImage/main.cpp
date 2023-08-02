
#include <iostream>
#include <opencv2/opencv.hpp>
#include <cmath>
#include <jsoncpp/json/json.h>
#include <jsoncpp/json/writer.h>
#include "ctpl.h"
#include <algorithm>
#include <vector>
#include <bits/stdc++.h>
#include <filesystem>

using namespace std;
using namespace cv;

void EdgeDetection_Child(int id, int i, cv::Mat* output_image, cv::Mat* classified_img2);
cv::Mat EdgeDetection(cv::Mat classified_img, int num_threads );
void Classification_Child(int id, int i, Mat* classified_img, Mat* edge_image, vector<vector<Point>>* contours_approx, vector<Vec4i>* hierarchy, vector <Vec3b>* contour_class);

string getATLASVersion(string input_json);
string getImgExt(string input_json);
double getMinPolygonArea(string input_json);

int main (int argc, char *argv[])
{
 
//parameters
//string input_directory = "../../Datasets/Rellis_3D_image_example/pylon_camera_node_label_color/";
string input_directory = "../../Datasets/Rellis_3D_pylon_camera_node_label_color/Rellis-3D/00000/pylon_camera_node_label_color/";
std::string input_json = "../../Mappings_RGB/Rellis3D_dataset.json";
int num_threads=std::thread::hardware_concurrency(); // number of parallel threads
//string output_directory = "../../Datasets/Rellis_3D_image_example/img_json/";
string output_directory = "../../Datasets/Rellis_3D_pylon_camera_node_label_color/00000_json/";
bool visualize=false;

// you can either get the default values in the json file or use custom values for the below parameters
// string ATLAS_version = "2.0.3";
string ATLAS_version = getATLASVersion(input_json);
// string ext(".png");
string ext = getImgExt(input_json);
// double min_polygon_area=100;
double min_polygon_area = getMinPolygonArea(input_json);

// set below parameters to true to save values or false to not save values in output json file
// note that input_img path relative to this build directory, the semantic class, entity number, and ATLAS version will be saved
bool saveArea=true;
bool savePolygonVertices=true;



//main code 
cout<<"starting"<<endl;
//get image files from directory
int k=0;
vector<string> img_files;
std::string input_image;
std::string output_json;

// put all image files from directory into vector for processing
for (auto &p : std::filesystem::recursive_directory_iterator(input_directory))
{
    if (p.path().extension() == ext)
    {
        
        k++;
        string temp_string=p.path().stem().string();
        
        img_files.push_back(p.path().stem().string());
        //cout << "file "<< k <<"  "<<temp_string << '\n';
        
    }
        
}

//read json file of rgb values for dataset
std::ifstream ifs(input_json);
Json::Reader reader;
Json::Value completeJsonData;
reader.parse(ifs,completeJsonData);

//std::cout<< "Complete JSON data: "<<std::endl<< completeJsonData<<std::endl;
std::vector<std::string> semantic_classes;
std::vector<cv::Vec3b> color_values;

for (auto const& id3 : completeJsonData["Color_Information"].getMemberNames()) 
{
//std::cout<<id3<<std::endl;
semantic_classes.push_back(id3);
cv::Vec3b temp_color;
temp_color[1] =  completeJsonData["Color_Information"][id3]["red_value"].asInt();    
temp_color[0] =  completeJsonData["Color_Information"][id3]["green_value"].asInt();
temp_color[2] =  completeJsonData["Color_Information"][id3]["blue_value"].asInt();
color_values.push_back(temp_color);
//cout<<temp_color<<endl;
}


// process each image file
ctpl::thread_pool p(num_threads);

for(int a=0; a<img_files.size(); a++)
{
    cout<<a<<endl;
    input_image = input_directory + img_files[a] + ext;
    output_json = output_directory + img_files[a] + ".json";

    //read input image
    cv::Mat segmented_img = cv::imread(input_image);

    //find edges in image
    cv::Mat edge_img=EdgeDetection(segmented_img, num_threads );
    

    //extract polygons from edge image
    // detectcontours 
    std::vector<cv::Vec4i> hierarchy;
    std::vector<std::vector<cv::Point>>contours_approx;
    findContours( edge_img, contours_approx, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE, cv::Point(0, 0) );

    //filter below size threshold
    for (int i=0 ; i<contours_approx.size(); i++)
    {
        int contour_temp_area=cv::contourArea(contours_approx[i]);
        if (contour_temp_area < min_polygon_area)
        {
            contours_approx[i].clear();                   
            contours_approx[i].push_back(cv::Point(0, 0));
        }
    }   

    cv::Mat drawing = cv::Mat::zeros( edge_img.size(), CV_8UC3 );
    std::vector <cv::Vec3b> contour_class(contours_approx.size()+1);
    //classify the detected contours
    // this function is multithreaded to improve speed
    for(int i = 0; i <contours_approx.size(); i++) 
    {
        if(contours_approx[i].size()>2)
        {
            p.push(Classification_Child,i,&segmented_img,&edge_img, &contours_approx, &hierarchy, &contour_class);
        }
    }  

    // wait until threadpool is finished here
    while(p.n_idle()<num_threads)
    {
        //cout<<" running threads "<< p.size()  <<" idle threads "<<  p.n_idle()  <<endl;
        //do nothing 
    }

    //cout<<"polygons colors"<<endl;
    std::ofstream file_id;
    file_id.open(output_json);
    Json::Value event; 
    // initialise JSON file
    event["input_img"] = input_image;
    event["ATLAS_version"] = ATLAS_version;
    int count =0; 
    Mat drawing2 = Mat::zeros( edge_img.size(), CV_8UC3 );
    for( int i = 0; i< contours_approx.size(); i++ )
    {
        if (contours_approx[i].size()>2)
        {
            
            Vec3b color = contour_class[i];
            
            
            auto test_trial =  std::find(color_values.begin(), color_values.end(), color);
            if ( test_trial != color_values.end() )
            {   

                Vec3b color2=cv::Vec3b(color[1],color[0],color[2]);
                int index = test_trial - color_values.begin();
                //cout<< semantic_classes[index] << "  has area "<< cv::contourArea(contours_approx[i]) <<endl;
                
                Json::Value vec(Json::arrayValue);
                for (int j = 0; j< contours_approx[i].size(); j++){
                    Json::Value arr(Json::arrayValue);
                    arr.append(contours_approx[i][j].x);
                    arr.append(contours_approx[i][j].y);
                    vec.append(arr);
                }                     
                //cout<<contours_approx[i]<<endl;
                event["entities"][count]["properties"]["entity_number"] = count;
                if (saveArea)
                {
                    event["entities"][count]["properties"]["pixel_area"]= cv::contourArea(contours_approx[i]) ;
                }
                if (i==0)
                {
                    event["entities"][count]["type"]= "Ballpark";
                    color2=cv::Vec3b(0,0,0);
                }
                else
                {
                    event["entities"][count]["type"]= semantic_classes[index] ;
                }
                if(savePolygonVertices)
                {
                    event["entities"][count]["geometry"]["type"] = "LineString";
                    event["entities"][count]["geometry"]["coordinates"]=vec;
                }
                count++;
                
                drawContours( drawing2, contours_approx, i, color2, FILLED, 8, hierarchy, 0, Point() );

            }
            else
            {   
                 cout<<color<<" not defined in json \n "<<endl;
                //return -2;
                Vec3b color2=cv::Vec3b(color[1],color[0],color[2]);
                               
                Json::Value vec(Json::arrayValue);
                for (int j = 0; j< contours_approx[i].size(); j++){
                    Json::Value arr(Json::arrayValue);
                    arr.append(contours_approx[i][j].x);
                    arr.append(contours_approx[i][j].y);
                    vec.append(arr);
                }                     
                //cout<<contours_approx[i]<<endl;
                event["entities"][count]["properties"]["entity_number"] = count;
                if (saveArea)
                {
                    event["entities"][count]["properties"]["pixel_area"]= cv::contourArea(contours_approx[i]) ;
                }
                if (i==0)
                {
                    event["entities"][count]["type"]= "Ballpark";
                    color2=cv::Vec3b(0,0,0);
                }
                else
                {
                    event["entities"][count]["type"]= "unknown_class" ;
                }
                if(savePolygonVertices)
                {
                    event["entities"][count]["geometry"]["type"] = "LineString";
                    event["entities"][count]["geometry"]["coordinates"]=vec;
                }
                count++;
                
                drawContours( drawing2, contours_approx, i, color2, FILLED, 8, hierarchy, 0, Point() );
            }
        }
    }

    //write results to output json file
    Json::StyledWriter styledWriter;
    file_id << styledWriter.write(event);
    file_id.close();  

    if (visualize)
    {
        //input image
        //cv::imshow("Image", segmented_img);
        //cv::waitKey(500);
        //detected edges
        //cv::imshow("Image", edge_img);
        //cv::waitKey(500);
        //convert opencv image BGR to RGB format 
        cvtColor( drawing2, drawing2, COLOR_BGR2RGB );
        //filtered polygons for output json file
        cv::imshow("Image", drawing2);
        cv::waitKey(200);
    }

}


cout<<"finished"<<endl;
    
return -1;
}

//-----------------------------------------------------------------------------








cv::Mat EdgeDetection(cv::Mat classified_img, int num_threads )
{
    // create a copy of the incoming image in terms of size (length and width) and initialize as an all black image
    cv::Mat output_image(classified_img.rows, classified_img.cols, CV_8UC1, cv::Scalar(0));
    // using 8 bit image so white pixel has a value of 255

    ctpl::thread_pool p(num_threads);
    for(int i = 0; i <classified_img.rows; i++) 
    {
        p.push(EdgeDetection_Child,i,&output_image,&classified_img);
    }  
    // wait until threadpool is finished here
    while(p.n_idle()<num_threads)
    {
        //cout<<" running threads "<< p.size()  <<" idle threads "<<  p.n_idle()  <<endl;
        //do nothing 
    }

    cv::Mat edge_img= output_image;
    return edge_img;
}

void EdgeDetection_Child(int id, int i, cv::Mat* output_image, cv::Mat* classified_img2)
{

    bool edge=false;
    cv::Vec3b temp_val, compare_val; // rgb value of image at a pixel 
    cv::Mat classified_img=*classified_img2;
        for(int j = 0; j < classified_img.cols; j++)
        {
              edge=false;
              
              if (i==0 || j==0 ||   i== classified_img.rows-1  || j==classified_img.cols-1)
              {
                // set boundaries of image to edge
                edge=true;
              }
              else
              {
                temp_val=classified_img.at<cv::Vec3b>(i,j); // in form (y,x) 
              
                // go through image pixel by pixel  and look at surrounding 8 pixels, if there is a difference in color between center and other pixels, then it is an edge 
                
                for (int a=-1; a<2; a++)
                {
                    for (int b=-1; b<2; b++)
                    {
                        compare_val=classified_img.at<cv::Vec3b>(i+a,j+b);
                        if (compare_val != temp_val)
                        {
                            edge=true;
                        }            
                    }           
                }        
              }
            
              if (edge)
              {
                  // set edge pixel to white
                  output_image->at<uchar>(i,j)=255;            
              }
         }
}  

void Classification_Child(int id, int i, Mat* classified_img, Mat* edge_image, vector<vector<Point>>* contours_approx, vector<Vec4i>* hierarchy, vector <Vec3b>* contour_class)
{
    Mat b_hist, g_hist, r_hist;
    int histSize = 256;
    float range[] = { 0, 256 }; //the upper boundary is exclusive
    const float* histRange[] = { range };
    bool uniform = true, accumulate = false;
    vector<Mat> bgr_planes;
    split( *classified_img, bgr_planes );
    Vec3b color_temp; 

     Mat drawing2 = Mat::zeros( edge_image->size(), CV_8UC1 );
     Scalar color = Scalar( 255);
     drawContours( drawing2, *contours_approx, i, color, FILLED, 8, *hierarchy, 0, Point() ); 
     calcHist( &bgr_planes[0], 1, 0, drawing2, b_hist, 1, &histSize, histRange, uniform, accumulate );
     calcHist( &bgr_planes[1], 1, 0, drawing2, g_hist, 1, &histSize, histRange, uniform, accumulate );
     calcHist( &bgr_planes[2], 1, 0, drawing2, r_hist, 1, &histSize, histRange, uniform, accumulate );
     int max_r=0, max_b=0, max_g=0;
     int max_r_loc=0, max_b_loc=0, max_g_loc=0;
     
     
        for (int j=0; j<256 ; j++)
        {
            if (r_hist.at<float>(j) > max_r)
            {
                max_r=r_hist.at<float>(j);
                max_r_loc=j;
                color_temp[1]=max_r_loc;
            }
            
            if (g_hist.at<float>(j) > max_g)
            {
                max_g=g_hist.at<float>(j);
                max_g_loc=j;
                color_temp[0]=max_g_loc;
            }
            
            if (b_hist.at<float>(j) > max_b)
            {
                max_b=b_hist.at<float>(j);
                max_b_loc=j;
                color_temp[2]=max_b_loc;
            }
      
        }
        (*contour_class)[i]=  color_temp;
}

string getATLASVersion(string input_json)
{
    
    //read json file of paramter valuet
    std::ifstream ifs(input_json);
    Json::Reader reader;
    Json::Value completeJsonData;
    reader.parse(ifs,completeJsonData);

    string result = completeJsonData["Processing_Properties"]["parameters"]["ATLAS_version"].asString();
    return result;

}

string getImgExt(string input_json)
{
    
    //read json file of paramter valuet
    std::ifstream ifs(input_json);
    Json::Reader reader;
    Json::Value completeJsonData;
    reader.parse(ifs,completeJsonData);

    string result = completeJsonData["Processing_Properties"]["parameters"]["img_extension"].asString();
    return result;

}

double getMinPolygonArea(string input_json)
{
    
    //read json file of paramter valuet
    std::ifstream ifs(input_json);
    Json::Reader reader;
    Json::Value completeJsonData;
    reader.parse(ifs,completeJsonData);

    double result = completeJsonData["Processing_Properties"]["parameters"]["min_polygon_size"].asDouble();
    return result;

}
