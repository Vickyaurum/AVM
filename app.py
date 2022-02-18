import numpy as np
from flask_restful import Api, Resource
from flask_cors import CORS
import AVM_Am
from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import re
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)
api=Api(app)

class projectDataValidator(object):
    def __init__(self,response={}):
        self.response=response
    def isTrue(self):
        errormessage=[]
        location=self.response.get("Location")
        try:
            if isinstance(location,int):
                raise Exception("Error")
        except Exception as e:errormessage.append("Invalid Input. Kindly enter a location")

        return errormessage

    def returnProjectData(self,data):
        try:
            client1 = MongoClient("mongodb+srv://AurumUser:latestPlacid@cluster0.icdds.mongodb.net/projectdescription?retryWrites=true&w=majority")
            db = client1['projectdescription']
            col=db['projectdescription']
            print("Db connected")
            doc = col.find(data)
            fa=[]
            for i in doc:
                if i['Project_Name'] in fa:
                    pass
                else:
                    print(i['Project_Name'],i['Location'])
                    fa.append(i['Project_Name'])
            print("PROOO",fa)
                    # return json.dumps(i['Project_Name'], indent=4, default=json_util.default)
            return {"Projects":fa}
        except:
            return "Couldnt connect to Database"

class getPuneProjectData(Resource):
    def get(self):
        return "Hello AVM USer"
    def post(self):
        data=json.loads(request.data)
        print(data)
        _instance = projectDataValidator(response=data)
        response=_instance.isTrue()

        if len(response)>0:
            _={
                "status":"error",
                "message":response
            },403
            return _
        else:
            # dbcol=_instance.dbConnect()
            val=_instance.returnProjectData(data)
            return val

api.add_resource(getPuneProjectData,"/project")


class gisvalidator(object):
    def __init__(self,response={}):
        self.response=response
    def isTrue(self):
        errormessage=[]
        try:
            location=self.response.get("Location")
            try:
                if isinstance(location,int):
                    raise Exception("Error")
            except Exception as e:errormessage.append("Invalid Input. Kindly Enter a location")
        except:
            lat=self.response.get("LAT")
            long=self.response.get("LNG")

            try:
                if isinstance(lat,str):
                    raise Exception("Error")
            except Exception as e:errormessage.append("Invalid Input, Kindly input A latitude")

            try:
                if isinstance(long,str):
                    raise Exception("Error")
            except Exception as e:errormessage.append("Invalid Input, Kindly input A longitude")

        return errormessage

    # def dbConnect(self):
    #     try:
    #         client1 = MongoClient("mongodb+srv://AurumUser:latestPlacid@cluster0.icdds.mongodb.net/gis?retryWrites=true&w=majority")
    #         db = client1['gis']
    #         col=db['gis_pune']
    #         print("Db connected")
    #     except:
    #         print("COULDNT CONNECT")
    #     return col

    def returnData(self,data):
        try:
            client1 = MongoClient("mongodb+srv://AurumUser:latestPlacid@cluster0.icdds.mongodb.net/gis?retryWrites=true&w=majority")
            db = client1['gis']
            col=db['gis_pune']
            print("Db connected")
            if "Location" in list(data.keys()):
                doc = col.find(data)
                print("RE",data)
                for i in doc:
                    return json.dumps(i, indent=4, default=json_util.default)
            elif "LAT" in list(data.keys()):
                lat=data['LAT']
                lng=data['LNG']
                vh=col.aggregate([
                             {
                              "$match":{
                                "$and":[

                                    {"LAT":lat},
                                    {"LNG":lng}
                                ]
                             }
                            }])
                c=[]
                for i in vh:
                    print(i)
                    c.append(i)
                    print("*"*100)
                    return json.dumps(i, indent=4, default=json_util.default)
        except:
            return "Couldnt connect to Database"



class getGISData(Resource):
    def get(self):
        return "Hello AVM GIS USer"
    def post(self):
        data=json.loads(request.data)
        print(data)
        _instance = gisvalidator(response=data)
        response=_instance.isTrue()

        if len(response)>0:
            _={
                "status":"error",
                "message":response
            },403
            return _
        else:
            # dbcol=_instance.dbConnect()
            val=_instance.returnData(data)
            return val

api.add_resource(getGISData,"/gis")



class dataValidator(object):
    def __init__(self,response={}):
        self.response=response

    def isTrue(self):
        errormessage=[]
        area=self.response.get("Area")
        bhk=self.response.get("BHK")
        bathroom=self.response.get("Bathroom")
        # balcony=self.response.get("Balcony")
        # best_gas_station=self.response.get("Best_Gas_station_count")
        # best_shopping_mall_count=self.response.get("Best_Shopping_mall_count")
        # Best_school_count=self.response.get("Best_school_count")
        # Best_Restaurant_count=self.response.get("Best_Restaurant_count")
        # Best_ATM_count=self.response.get("Best_ATM_count")
        # Best_Hospital_count=self.response.get("Best_Hospital_count")
        # ATM_count=self.response.get("ATM_count")
        # Gas_station_count=self.response.get("Gas_station_count")
        # Shopping_mall_count=self.response.get("Shopping_mall_count")
        # School_count=self.response.get("School_count")
        # Hospital_count=self.response.get("Hospital_count")
        # Restaurant_count=self.response.get("Restaurant_count")
        # Other_amenities=self.response.get("Other_amenities")
        Exterior_amenities=self.response.get("Exterior_amenities")
        Interior_amenities=self.response.get("Interior_amenities")
        Windows_amenity=self.response.get("Windows_amenity")
        Doors_amenity=self.response.get("Doors_amenity")
        Electrical_amenity=self.response.get("Electrical_amenity")
        Balcony_amenity=self.response.get("Balcony_amenity")
        Toilet_amenity=self.response.get("Toilet_amenity")
        Kitchen_amenity=self.response.get("Kitchen_amenity")
        Other_Bedroom_amenity=self.response.get("Other_Bedroom_amenity")
        Master_Bedroom_amenity=self.response.get("Master_Bedroom_amenity")
        Living_dining_room_amenity=self.response.get("Living_dining_room_amenity")
        Building_amenity=self.response.get("Building_amenity")
        location=self.response.get("location")
        # Project_Name=self.response.get("Project_Name")

        ## area empty and string
        try:
            if isinstance(area,str):
                raise Exception("Error")
        except Exception as e:errormessage.append("Area Field invalid. Please enter a numerical value")

        ## bhk empty and string
        try:
            if isinstance(bhk,str):
                raise Exception("Error")
        except Exception as e:errormessage.append("BHK Field invalid. Please enter a numerical value")

        # ## bhk empty and string
        # try:
        #     if isinstance(balcony,str):
        #         raise Exception("Error")
        # except Exception as e:errormessage.append("Balcony Field invalid. Please enter a numerical value")

        ## bhk empty and string
        try:
            if isinstance(bathroom,str):
                raise Exception("Error")
        except Exception as e:errormessage.append("Bathroom Field invalid. Please enter a numerical value")

        ## bhk and area incompatibility
        try:
            if area <= 500 and bhk>2:
                raise Exception("Error")
            elif area<=847 and bhk>3:
                raise Exception("Error")
            elif area<=1440 and bhk>4 and bhk<=1:
                raise Exception("Error")
            elif area<=2500 and bhk>5 and bhk<=2:
                raise Exception("Error")
            elif area<=3200 and bhk>6 and bhk<=3:
                raise Exception("Error")
            elif area>3000 and bhk<=3:
                raise Exception("Error")
        except Exception as e:errormessage.append("BHK and area are not compatible")


        # ## balcony and area incompatibility
        # try:
        #     if area <= 500 and balcony>2:
        #         raise Exception("Error")
        #     elif area<=847 and balcony>3:
        #         raise Exception("Error")
        #     elif area<=1440 and balcony>4:
        #         raise Exception("Error")
        #     elif area<=2500 and balcony>5:
        #         raise Exception("Error")
        #     elif area<=3200 and balcony>5:
        #         raise Exception("Error")
        # except Exception as e:errormessage.append("Balcony and area are not compatible")


        ## bhk and area incompatibility
        try:
            if area <= 500 and bathroom>2:
                raise Exception("Error")
            elif area<=847 and bathroom>3:
                raise Exception("Error")
            elif area<=1440 and bathroom>4 and bathroom<=1:
                raise Exception("Error")
            elif area<=2500 and bathroom>5 and bathroom<=2:
                raise Exception("Error")
            elif area<=3200 and bathroom>6 and bathroom<=3:
                raise Exception("Error")
        except Exception as e:errormessage.append("Bathroom and area are not compatible")

        return errormessage

    def predict(self,data):
        regressor = joblib.load(r"C:\Users\Yogesh.Tiwari\PycharmProjects\pythonProject\Positive_Per_Sq_Pune_pk_15feb.pkl")
        dd=pd.read_csv(r"C:\Users\Yogesh.Tiwari\PycharmProjects\pythonProject\ABC_ref.csv")
        gi_da=pd.read_excel(r"C:\Users\Yogesh.Tiwari\PycharmProjects\pythonProject\GIS_LOC_FEATURE_PUNE.xlsx")
        event = data
        print(event)
        hello=[]
        for i,v in event.items():
            hello.append(v)

        features = hello[0:16]
        # features = hello[0:31]
        final_val=features[0:3]

        # gis_listy=hello[4:16]


        print("Features**********************\n",features)
        pr=AVM_Am.get_proj(features)
        print("PR VALUES",type(pr),pr)
        gis_feat=['Best_school_count', 'Best_Restaurant_count', 'Best_ATM_count', 'Best_Hospital_count', 'ATM_count', 'Shopping_mall_count', 'School_count', 'Hospital_count', 'Restaurant_count']
        exterior_am=['Exterior_ Asian Paint', 'Exterior_ Texture Paint', 'Exterior_ Apex Paint', 'Exterior_ Acrylic Emulsion Paint', 'Exterior_ Gypsum Finish', 'Exterior_ Apex Weatherproof Emulsion Paint', 'Exterior_ Emulsion Paint', 'Exterior_ Good Quality Paint', 'Exterior_ Weather Proof Paint', 'Exterior_ Water Resistant Paint', 'Exterior_ High Quality Texture Paint', 'Exterior_ POP Finish', 'Exterior_ Plastic Emulsion Paint']
        interior_am=['Interior_ Acrylic Paint', 'Interior_ Plastic Paint', 'Interior_ Emulsion Paint', 'Interior_ Acrylic Emulsion Paint', 'Interior_ Plastic Emulsion Paint', 'Interior_ Texture Paint', 'Interior_ POP Finish', 'Interior_ Paint, Distemper', 'Interior_ Sand Faced Plaster', 'Interior_ Cement Based Paint', 'Interior_ Semi Acrylic Paint', 'Interior_ Good Quality Paint', 'Interior_ Standard Paint', 'Interior_ Acrylic Emulsion Paint on POP Punning']
        window_am=['Windows_ Aluminium Powder Coated Windows', 'Windows_ 3 Track UPVC Windows with SS Mosquito Net', 'Windows_ Aluminium Sliding Windows', 'Windows_ Anodized Aluminium Sliding', 'Windows_ Aluminium / UPVC / HardWood', 'Windows_ Powder coated aluminium sliding windows', 'Windows_ Aluminium Frames with Glazed Shutters', 'Windows_ Powder Coated Aluminum / UPVC Frames', 'Windows_ 2 Track UPVC Sliding Window with Mosquito Mesh Shutter', 'Windows_ Anodised / Powder Coated Aluminium Sliding Windows', 'Windows_ Standard', 'Windows_ M.S. Frame and Flush Door Shutter', 'Windows_ UPVC / Aluminium Windows', 'Windows_ Standard Windows', 'Windows_ Aluminum Sliding Window with Mosquito Mesh Shutters', 'Windows_ French Windows']
        door_am=['Doors_ Veneered Door', 'Doors_ Moulded Designer Door', 'Doors_ Designer Door', 'Doors_ Decorative Flush Door', 'Doors_ Wooden Frame', 'Doors_ Elegant Door', 'Doors_ Pre Engineered Steel Frame with Wooden Shutters', 'Doors_ Aluminium with Wooden Shade', 'Doors_ Wood Frame', 'Doors_ Heavy Duty Wooden Laminated Doors', 'Doors_ Standard', 'Doors_ Decorative Flush with Hardwood Door Frames', 'Doors_ Beach Wood Frame', 'Doors_ Teak Wood Frame and Shutter']
        electrical_am=['Electrical_ Concealed copper wiring', 'Electrical_ Concealed Copper Wiring with MCB/ ELCB', 'Electrical_ Copper Wiring in PVC Concealed Conduit', 'Electrical_ Concealed Copper Wiring', 'Electrical_ Havells/Anchor Make', 'Electrical_ Standard', 'Electrical_ Branded Concealed Copper Wiring with MCB / ELCB']
        balcony_am=['Balcony_ Anti Skid Tiles', 'Balcony_ Vitrified Tiles', 'Balcony_ Anti Skid Vitrified Tiles', 'Balcony_ Marble Granite Tiles', 'Balcony_ Italian Marble']
        toilet_am=['Toilets_ Anti Skid Tiles', 'Toilets_ CP Fittings of Jaquar / Marc or Equivalent', 'Toilets_ Branded CP Fittings & Sanitary Ware, Anti-Skid Tiles', 'Toilets_ Branded CP Fittings and Sanitary Ware', 'Toilets_ Ceramic Tiles Dado', 'Toilets_ Vitrified Tiles', 'Toilets_ Provision For Exhaust Fan', 'Toilets_ Anti Skid Tiles Dado', 'Toilets_ Sanitary fittings', 'Toilets_ Vitrified / Ceramic Tiles Dado', 'Toilets_ Branded CP Fitting', 'Toilets_ Kohler/Roca/American Standard or Equivalent Make', 'Toilets_ Ceramic Tiles Dado up to Lintel Level', 'Toilets_ Anti Skid Vitrified Tiles', 'Toilets_ Designer Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Sanitary Ware / Parryware / Hindware or Equivalent Sanitary Fittings', 'Toilets_ Matt Finish Tiles', 'Toilets_ Marble Granite Tiles', 'Toilets_ Full Height Designer Tiles', 'Toilets_ ISI Branded Chromium Plated Tap', 'Toilets_ Parryware or Equivalent Sanitary Fittings', 'Toilets_ Provision for Geyser', 'Toilets_ Concealed Plumbing with Hot & Cold Mixer', 'Toilets_ Glazed Tiles', 'Toilets_ Vitrified Tiles (Kajaria)', 'Toilets_ High Quality CP Fittings', 'Toilets_ Italian Marble', 'Toilets_ Acid Resistant Tiles', 'Toilets_ EWC', 'Toilets_ Glazed Tiles Dado Up to Door Height', 'Toilets_ Granite Counter', 'Toilets_ Marble Flooring', 'Toilets_ Imported Marble Dado', 'Toilets_ Imported Marble', 'Toilets_ Mirror']
        kitchen_am=['Kitchen_ Granite platform with stainless steel sink', 'Kitchen_ Ceramic Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ - Granite counter in kitchen area', 'Kitchen_ Anti Skid Tiles Dado', 'Kitchen_ Modular Kitchen', 'Kitchen_ Stainless Steel Sink', 'Kitchen_ Ceramic Tiles Dado', 'Kitchen_ Italian Marble', 'Kitchen_ Branded CP fittings', 'Kitchen_ Vetrified tile flooring', 'Kitchen_ Designer Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ Vitrified tiles on floor', 'Kitchen_ Ceramic Tiles', 'Kitchen_ Double bowl stainless steel sink', 'Kitchen_ Ceramic / Glazed Tiles Dado', 'Kitchen_ Concealed Plumbing with Premium Quality CP Fitting', 'Kitchen_ Dado Designer Wall Tiles', 'Kitchen_ Black Granite Platform', 'Kitchen_ Polished Granite Platform with Stainless Steel Sink', 'Kitchen_ Provision for Water Purifier', 'Kitchen_ 12 x 12 ceramic tiles', 'Kitchen_ Moduler Kitchen with Chimney & HOB', 'Kitchen_ Marble Granite Tiles', 'Kitchen_ C. P. Fittings.', 'Kitchen_ Granite Platform with Stainless Steel Sink and Drain Board', 'Kitchen_ Vitrified tile flooring in all rooms', 'Kitchen_ Vitrified tile flooring', 'Kitchen_ Italian Modular Cabinets', 'Kitchen_ RO System', 'Kitchen_ Floor Vitrified tile', 'Kitchen_ Designer glazed tile upto full height', 'Kitchen_ Green Marble', 'Kitchen_ Dishwasher', 'Kitchen_ Provision For Chimney And Water Purifier', 'Kitchen_ - Green marble/granite', 'Kitchen_ Modular Kitchen with Stainless Steel Sink', 'Kitchen_ Granite Flooring', 'Kitchen_ Ceramic Tiles Dado Till 600 mm above the Counter', 'Kitchen_ Elegant Vitrified Tiles', 'Kitchen_ Granite Platform', 'Kitchen_ Ceramic Tiles Dado above Working Platform', 'Kitchen_ Full marble flooring', 'Kitchen_ Anti Skid Vitrified Tiles']
        other_bedroom_am=['Other_Bedroom_ Vitrified Flooring', 'Other_Bedroom_ Marble Flooring', 'Other_Bedroom_ Vitrified tiles', 'Other_Bedroom_ 1mx1m vitrified tiles in bedrooms', 'Other_Bedroom_ Wooden Flooring', 'Other_Bedroom_ Vitrified floor tiles', 'Other_Bedroom_ Laminated Wooden', 'Other_Bedroom_ Granamite Tiles', 'Other_Bedroom_ Vitrified Flooring In Other Bedrooms', 'Other_Bedroom_ Floors Vitrified tiles flooring', 'Other_Bedroom_ Hardwood Flooring', 'Other_Bedroom_ All Bedrooms Imported engineered wooden flooring', 'Other_Bedroom_ Italian Marble', 'Other_Bedroom_ 800 x 800 vitrified ceramic tiles flooring', 'Other_Bedroom_ All bedrooms with wooden floorings', 'Other_Bedroom_ Marble Granite Tiles', 'Other_Bedroom_ Marble flooring in all bedrooms']
        masterbedroom_am=['Master_Bedroom_ Vitrified Flooring', 'Master_Bedroom_ - Master bedroom wooden flooring / other bedrooms vitrified tiles', 'Master_Bedroom_ Marble Flooring', 'Master_Bedroom_ Laminated Wooden Flooring', 'Master_Bedroom_ Wooden flooring', 'Master_Bedroom_ Best Quality Vitrified Tiles', 'Master_Bedroom_ Vitrified Tiled Flooring', 'Master_Bedroom_ - Wooden flooring in master bedroom', 'Master_Bedroom_ Laminated Wooden', 'Master_Bedroom_ 2 x 2 wooden finish vitrified tiles in Master bedroom', 'Master_Bedroom_ Granamite Tiles', 'Master_Bedroom_ Flooring Vitrified tiles', 'Master_Bedroom_ Master Bedrooms Wooden Flooring', 'Master_Bedroom_ Hardwood Flooring', 'Master_Bedroom_ Italian Marble', 'Master_Bedroom_ Engineered Wooden Flooring', 'Master_Bedroom_ Wooden finish vitrified tiles in master bedroom', 'Master_Bedroom_ 2 x 2 vitrified tiles drawing room , dining room, all bed rooms, kitchen and other area, wooden flooring in master bedroom', 'Master_Bedroom_ Marble Granite Tiles']
        living_dining_am=['Living_Dining_ Anti Skid Tiles', 'Living_Dining_ Marble Flooring', 'Living_Dining_ Morbonite Tiles', 'Living_Dining_ Anti Skid Vitrified Tiles', 'Living_Dining_ Marble Granite Tiles', 'Living_Dining_ Imported Marble', 'Living_Dining_ Granamite Tiles', 'Living_Dining_ Elegant Vitrified Tiles', 'Living_Dining_ Kota Stone', 'Living_Dining_ Ceramic Tiles', 'Living_Dining_ Italian marble', 'Living_Dining_ Acid Resistant Tiles']
        building_am=['Building_Entrance Lobby', 'Building_Video Door Security', 'Building_Gazebo', 'Building_Open Parking', 'Building_Community Buildings', 'Building_Badminton Court', 'Building_Electrification(Transformer, Solar Energy etc)', 'Building_Fire Protection And Fire Safety Requirements', 'Building_Open Car Parking', 'Building_Multipurpose Hall', 'Building_Solar Lighting', 'Building_Intercom', 'Building_Multipurpose Room', 'Building_Solar Water Heating', 'Building_Waiting Lounge', 'Building_Infinity Pool', 'Building_Hospital', 'Building_Visitor Parking', "Building_Kid's Pool", 'Building_Banquet Hall', 'Building_Water Storage', 'Building_Jacuzzi', 'Building_Reflexology Park', 'Building_Staff Quarter', 'Building_Vaastu Compliant', 'Building_Spa/Sauna/Steam', 'Building_Squash Court', 'Building_Garbage Disposal', 'Building_Paved Compound', 'Building_Card Room', 'Building_Water Softner Plant', 'Building_Sun Deck', 'Building_Reading Lounge', 'Building_Laundromat', 'Building_Cricket Pitch', 'Building_RO Water System', 'Building_Valet Parking', 'Building_Service Lift', 'Building_Garden', 'Building_Fire Retardant Structure', 'Building_Lawn Tennis Court', 'Building_Pet Grooming', 'Building_Changing Room', 'Building_Salon', 'Building_Mini Theatre', 'Building_Golf Course', 'Building_Bar/Chill-out Lounge', 'Building_Aerobics Room', 'Building_Terrace Garden', 'Building_Open Air Theatre', 'Building_Flower Garden', 'Building_Spa', 'Building_Fountains', 'Building_Business Center', 'Building_Steam Room', 'Building_Restaurants/ Cafeterias', 'Building_Multi - Level Parking', 'Building_Billiards/Snooker Table', 'Building_Letter Box', 'Building_High Speed Elevators', 'Building_Semi Open Car Parking', 'Building_Theme Park', 'Building_Football Field', 'Building_Medical Facilities', 'Building_Medical Store/Pharmacy', 'Building_Doctor on call', 'Building_Foosball', 'Building_Smoke Detectors', 'Building_Reception/Waiting Room', 'Building_Concierge Service', 'Building_High-tech alarm system', 'Building_Manicured Garden', 'Building_DG Availability', 'Building_Beach Volley Ball Court', 'Building_Fire Alarm', 'Building_Water Supply', 'Building_Gas Pipeline', 'Building_Bore and Municipal Water', 'Building_Food Court', 'Building_Boom Barriers', 'Building_Helipad', 'Building_Board Games', 'Building_Automated Car Wash', 'Building_Anti-termite Treatment', 'Building_Sun Bathing', 'Building_Nature Club', 'Building_Cineplex', 'Building_Full Power Backup', 'Building_Advanced Security', 'Building_Sub-Station', 'Building_Club Rooftop']
        location=['Anand Nagar', 'Aundh', 'BT Kawade Road', 'Balewadi', 'Baner', 'Bavdhan', 'Bibwewadi', 'Central Mumbai Suburbs', 'Chandan Nagar', 'Gahunje', 'Ghorpadi', 'Koregaon Park', 'Kothrud', 'Magarpatta City', 'Mahalunge', 'Pashan', 'Pashan Road', 'Paud Road', 'Pimple Nilakh', 'Shaniwar Peth', 'Sinhagad Road', 'Viman Nagar', 'Wadgaon Sheri', 'Wanowrie', 'Wanwadi']


        # gis_feat=['Best_Gas_station_count', 'Best_Shopping_mall_count', 'Best_school_count', 'Best_Restaurant_count', 'Best_ATM_count', 'Best_Hospital_count', 'ATM_count', 'Gas_station_count', 'Shopping_mall_count', 'School_count', 'Hospital_count', 'Restaurant_count']
        #other_am=['Others_Others', 'Others_ Standard', 'Others_ Standard Fittings', 'Others_']
        # exterior_am=['Exterior_ Acrylic Paint', 'Exterior_ Asian Paint', 'Exterior_ Paint, Distemper', 'Exterior_ Sand Faced Plaster', 'Exterior_ Texture Paint', 'Exterior_ Apex Paint', 'Exterior_ Weather proof paint', 'Exterior_ Acrylic Emulsion Paint', 'Exterior_ Gypsum Finish', 'Exterior_ Apex Weatherproof Emulsion Paint', 'Exterior_ Emulsion Paint', 'Exterior_ Superior quality cement paint for external walls and oil bound for internal walls', 'Exterior_ Good Quality Paint', 'Exterior_ Oil Bound Distemper Paint', 'Exterior_ Semi Acrylic Paint', 'Exterior_ ACE Paint', 'Exterior_ Weather Proof Paint', 'Exterior_ Water Resistant Paint', 'Exterior_ Exterior Paint', 'Exterior_ High Quality Texture Paint', 'Exterior_ Cement Paint', 'Exterior_ Plastic Paint', 'Exterior_ Cement Based Paint', 'Exterior_ POP Finish', 'Exterior_ Exterior Grade Acrylic Emulsion', 'Exterior_ Acrylic Paints', 'Exterior_ Plastic Emulsion Paint', 'Exterior_ Water Proof Cement Paint', 'Exterior_ Standard Paints', 'Exterior_ Texture Paints', 'Exterior_ Weather Coat Paint', 'Exterior_ Superior Paint Finish', 'Exterior_ Plastic Paints', 'Exterior_', 'Exterior_ Weather Proof Texture Paint', 'Exterior_ Sandfaced Paints', 'Exterior_ Oil Bound Distemper']
        # interior_am=['Interior_ Oil Bound Distemper', 'Interior_ Putty on Walls', 'Interior_ Acrylic Paint', 'Interior_ Gypsum Finish', 'Interior_ Plaster & OBD', 'Interior_ Plastic Paint', 'Interior_ Emulsion Paint', 'Interior_ Acrylic Emulsion Paint', 'Interior_ Plastic Emulsion Paint', 'Interior_ Texture Paint', 'Interior_ Acrylic Emulsion Paint with Putty', 'Interior_ ACE Paint', 'Interior_ POP Finish', 'Interior_ Luster Paint', 'Interior_ Paint, Distemper', 'Interior_ Sand Faced Plaster', 'Interior_ POP Punning with OBD Finish', 'Interior_ Cement Based Paint', 'Interior_ Semi Acrylic Paint', 'Interior_ Asian Paint', 'Interior_ Good Quality Paint', 'Interior_ OBD Paints', 'Interior_ Acrylic Emulsion Paints', 'Interior_ Acrylic OBD Paints', 'Interior_ Plastic Emulsion Paints', 'Interior_ Oil Bound Paints', 'Interior_ OBD', 'Interior_ Luster Paint and Plastic Paint', 'Interior_ Standard Paints', 'Interior_ Standard Paint', 'Interior_ Acrylic Emulsion Paint on POP Punning', 'Interior_', 'Interior_ Gypsum Paints']
        # window_am=['Windows_ Powder Coated Aluminium Sliding Window', 'Windows_ 3 Track Powder Coated Aluminium Windows', 'Windows_ Aluminium Powder Coated Windows', 'Windows_ Powder Coated Aluminium Sliding', 'Windows_ 3 Track UPVC Windows with SS Mosquito Net', 'Windows_ UPVC Sliding Windows', 'Windows_ Aluminium Sliding Windows', 'Windows_ Aluminium Powder Coated Windows With Mosquito Mesh', 'Windows_ Anodized Aluminium Sliding with M.S Grill', 'Windows_ Aluminium Powder Coated Glazed Windows', 'Windows_ Aluminium Powder Coated 3-Track Sliding with Reflective Glass', 'Windows_ Anodized Aluminium Sliding', 'Windows_ Aluminium / UPVC / HardWood', 'Windows_ Powder coated aluminium sliding windows', 'Windows_ Powder Coated / Anodized Aluminium Sliding Windows', 'Windows_ Aluminium Frames with Glazed Shutters', 'Windows_ Powder coated aluminum sliding windows with safety grills and window sills', 'Windows_ Powder Coated Aluminum / UPVC Frames', 'Windows_ UPVC windows', 'Windows_ Aluminium Sliding', 'Windows_ Aluminium windows', 'Windows_ High Quality Aluminium Sliding Windows', 'Windows_ UPVC Windows with Granite Sills', 'Windows_ 2 Track UPVC Sliding Window with Mosquito Mesh Shutter', 'Windows_ Powder coated aluminium windows', 'Windows_ Anodised aluminium windows with mosquito nets', 'Windows_ Anodized aluminium windows', 'Windows_ Powder Coated Aluminium Sliding Windows', 'Windows_ Anodised / Powder Coated Aluminium Sliding Windows', 'Windows_ Powder Coated Aluminium Glazing', 'Windows_ Anodised Aluminium Window with MS Safety Grill & Mosquito Mesh', 'Windows_ Powder Coated Aluminium Sliding Windows with Mosquito Nets', 'Windows_ Standard Fittings', 'Windows_ Powder Coated Windows with Grills', 'Windows_ Powder Coated Aluminium Sliding Window With Mosquito Mesh, M.S. Safety Grill For Windows', 'Windows_ Standard', 'Windows_ M.S. Frame and Flush Door Shutter', 'Windows_ Anodized / Powder Coated Glazed Aluminium', 'Windows_ UPVC / Aluminium Windows', 'Windows_ Standard Windows', 'Windows_', 'Windows_ Aluminum Sliding Window with Mosquito Mesh Shutters', 'Windows_ Powder Coated Aluminium Windows', 'Windows_ French Windows']
        # door_am=['Doors_ Decorative Laminated Door', 'Doors_ Laminated Flush Door', 'Doors_ Decorative Main Door', 'Doors_ Aluminium/UPVC Doors', 'Doors_ Hard Wood Frame', 'Doors_ Veneered Door', 'Doors_ Both Side Laminated Flush Door', 'Doors_ Moulded Designer Door', 'Doors_ Designer Door', 'Doors_ Decorative Flush Door', 'Doors_ Decorative with Wooden Frame', 'Doors_ Wooden Frame', 'Doors_ Elegant Door', 'Doors_ Wooden Door with Teak Wood Finish', 'Doors_ Teak Wood Doors', 'Doors_ Decorative Door with Quality Brass Fittings Safety Lock', 'Doors_ Flush Door', 'Doors_ Decorative Laminate', 'Doors_ Pre Engineered Steel Frame with Wooden Shutters', 'Doors_ Decorative with Brass Fittings', 'Doors_ Veneer Flush Doors', 'Doors_ Teak Veneered / Laminated Flush Door', 'Doors_ Aluminium with Wooden Shade', 'Doors_ Wood Frame', 'Doors_ Verneer Finish Main Door', 'Doors_ Laminated Frame Doors', 'Doors_ Wooden Doors', 'Doors_ Moulded Skin Doors', 'Doors_ Teak Wood Frame', 'Doors_ Decorative Wooden Frame Door', 'Doors_ Standards Quality Doors', 'Doors_ Heavy Duty Wooden Laminated Doors', 'Doors_ Standard Fittings', 'Doors_ Laminated Doors', 'Doors_ Laminate On Both Sides With Branded Locks', 'Doors_ Laminated Flush Doors', 'Doors_ Standard', 'Doors_ Moduled Doors', 'Doors_ Decorative Flush with Hardwood Door Frames', 'Doors_ Beach Wood Frame', 'Doors_', 'Doors_ Teak Wood Frame and Shutter', 'Doors_ Decorativ Door', 'Doors_ Wooden Fittings']
        # electrical_am=['Electrical_ Concealed copper wiring', 'Electrical_ Concealed Copper Wiring with Adequate Points', 'Electrical_ Concealed Copper Wiring with Circuit Breakers', 'Electrical_ Concealed Fire Resistant Copper Wiring', 'Electrical_ Concealed Copper Wiring with MCB/ ELCB', 'Electrical_ Copper Wiring in PVC Concealed Conduit', 'Electrical_ Concealed Copper Wiring', 'Electrical_ Havells/Anchor Make', 'Electrical_ Standard', 'Electrical_ ISI Copper Wiring in PVC Concealed Conduit', 'Electrical_ Finolex or Equivalent Cables and Wiring', 'Electrical_ Concealed Copper Electric Wiring with Essential Points', 'Electrical_ Concealed Copper Wirings', 'Electrical_ Standard Fittings', 'Electrical_ Branded Concealed Copper Wiring with MCB / ELCB', 'Electrical_ Concealed Copper Wirings with Modular Switches', 'Electrical_ Legrand / Equivalent Electrical Switches', 'Electrical_ Electrical Switches Of Branded Make', 'Electrical_', 'Electrical_ Concealed Wirings with Modular Switches']
        # balcony_am=['Balcony_ Anti Skid Tiles', 'Balcony_ Ceramic Tiles', 'Balcony_ Vitrified Tiles', 'Balcony_ Anti skid ceramic tiles', 'Balcony_ Designer Tiles', 'Balcony_ Anti Skid Vitrified Tiles', 'Balcony_ Rustic Tiles', 'Balcony_ Marble Granite Tiles', 'Balcony_ Italian Marble', 'Balcony_ Standard', 'Balcony_ Anti-Skid Flooring', 'Balcony_ Johnson/Vermor Tiles', 'Balcony_ Wooden Flooring', 'Balcony_', 'Balcony_ Standard Floorings']
        # toilet_am=['Toilets_ Anti Skid Tiles', 'Toilets_ CP Fittings of Jaquar / Marc or Equivalent', 'Toilets_ Designer Tiles Dado', 'Toilets_ Designer Bath Fittings', 'Toilets_ Anti Skid Ceramic Tiles', 'Toilets_ Branded CP Fittings & Sanitary Ware, Anti-Skid Tiles', 'Toilets_ Ceramic Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Ceramic Tiles', 'Toilets_ Ceramic Tiles and Border', 'Toilets_ Branded CP Fittings and Sanitary Ware', 'Toilets_ Ceramic Tiles Dado', 'Toilets_ Vitrified Tiles', 'Toilets_ Provision For Exhaust Fan', 'Toilets_ Anti Skid Tiles Dado', 'Toilets_ CP fittings', 'Toilets_ Sanitary fittings', 'Toilets_ Vitrified / Ceramic Tiles Dado', 'Toilets_ Branded CP Fitting', 'Toilets_ Designer Tiles Dado up to Lintel Level', 'Toilets_ Kohler/Roca/American Standard or Equivalent Make', 'Toilets_ Ceramic Tiles Dado up to Lintel Level', 'Toilets_ Glazed Tiles Dado', 'Toilets_ Branded Sanitary Fittings', 'Toilets_ Tile Dado up to 7 Feet/Lintel Height.', 'Toilets_ CP Fittings from Essco or Equivalent Make', 'Toilets_ Glazed Tiles Dado up to Lintel Level', 'Toilets_ Branded CP Fittings with Hot & Cold Mixer', 'Toilets_ Designer Tiles Dado up to Door Height', 'Toilets_ GI / CPVC / PPR Pipes', 'Toilets_ Anti Skid Vitrified Tiles', 'Toilets_ Good Quality CP Fittings of Jaquar or Equivalent', 'Toilets_ Designer Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Premium CP Fittings', 'Toilets_ Hindware / Parryware or Equivalent Sanitary Fittings', 'Toilets_ Sanitary Ware / Parryware / Hindware or Equivalent Sanitary Fittings', 'Toilets_ Matt Finish Tiles', 'Toilets_ Single Lever CP Brass Fittings', 'Toilets_ Premium Sanitary Fittings', 'Toilets_ Provision for exhaust fan and anti-skid flooring', 'Toilets_ Concealed plumbing with premium quality CF fittings', 'Toilets_ Hot and Cold Water Mixer', 'Toilets_ Marble Granite Tiles', 'Toilets_ Full Height Designer Tiles', 'Toilets_ Provision for Wash Basin', 'Toilets_ ISI Branded Chromium Plated Tap', 'Toilets_ Chrome Plated Fittings', 'Toilets_ Glazed Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Parryware or Equivalent Sanitary Fittings', 'Toilets_ European Water Closet', 'Toilets_ Provision for Geyser', 'Toilets_ Dado of Glazed /Ceramic Tiles', 'Toilets_ Wash Basin', 'Toilets_ Concealed Plumbing', 'Toilets_ Concealed Plumbing with Hot & Cold Mixer', 'Toilets_ Ant Skid Ceramic Tiles', 'Toilets_ Jaguar Fittings', 'Toilets_ Designer Tiles on Dado upto Door Height', 'Toilets_ Cera / Equivalent Sanitary Fittings', 'Toilets_ Superior Quality Ceramic Tiles up to False Ceiling', 'Toilets_ Glazed Tiles', 'Toilets_ Vitrified Tiles (Kajaria)', 'Toilets_ High Quality CP Fittings', 'Toilets_ CP Fittings', 'Toilets_ Dado Tiles', 'Toilets_ Standard Fittings', 'Toilets_ Sanitary ware of Parry ware or equivalent', 'Toilets_ Sanitary Fittings', 'Toilets_ Branded Bathroom Fittings', 'Toilets_ Italian Marble', 'Toilets_ Acid Resistant Tiles', 'Toilets_ Standard Paints', 'Toilets_ EWC', 'Toilets_ Glazed Tiles Dado Up to Door Height', 'Toilets_ Ceramic Dado Tiles', 'Toilets_ Standard', 'Toilets_ Glazed Dado Tiles', 'Toilets_ Granite Counter', 'Toilets_ Toto / Equivalent Bathroom Fittings', 'Toilets_ Anti-Skid Flooring', 'Toilets_ Provision For Exhaust In Bathrooms, C.P. & Sanitary Fittings Of Branded Make, Glass Divider In Master Bathroom', 'Toilets_ Marble Flooring', 'Toilets_ Imported Marble Dado', 'Toilets_ Imported Marble', 'Toilets_ Full Height Tiles', 'Toilets_ Johnson/Vermor Tiles', 'Toilets_ Glazed Ceramic Tiles', 'Toilets_ Mirror', 'Toilets_ Combination of Ceramic/Vitrified Tiles Dado', 'Toilets_', 'Toilets_ Provision for Solar System', 'Toilets_ Designer Dado Tiles']
        # kitchen_am=['Kitchen_ Vitrified Tiles', 'Kitchen_ Exhaust Fan', 'Kitchen_ Glazed Tiles Dado', 'Kitchen_ Granite platform with stainless steel sink', 'Kitchen_ Provision For Water Purifier and Exhaust Fan', 'Kitchen_ Ceramic Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ - Granite counter in kitchen area', 'Kitchen_ Anti Skid Tiles Dado', 'Kitchen_ Designer Tiles Dado', 'Kitchen_ Vitrified Flooring', 'Kitchen_ Modular Kitchen', 'Kitchen_ Stainless Steel Sink', 'Kitchen_ Ceramic Tiles Dado', 'Kitchen_ Ceramic tiles dado upto lintel level', 'Kitchen_ Italian Marble', 'Kitchen_ Designer Tiles Dado up to Lintel Level', 'Kitchen_ Branded CP fittings', 'Kitchen_ Ceramic Tiles Dado up to Lintel Level', 'Kitchen_ Vetrified tile flooring', 'Kitchen_ Almirah / Cabinet (No HOB & CHIMNEY)', 'Kitchen_ Designer Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ Glazed Tiles above Platform', 'Kitchen_ Marble Flooring', 'Kitchen_ Vitrified tiles on floor', 'Kitchen_ Tiles Dado up to Beam Level over Platform', 'Kitchen_ Chimney', 'Kitchen_ Ceramic Tiles', 'Kitchen_ Glazed Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ Granite Platform with Stainless Steel Sink', 'Kitchen_ Granite platform', 'Kitchen_ - Vitrified flooring', 'Kitchen_ Double bowl stainless steel sink', 'Kitchen_ Glazed Tiles Dado up to Lintel Level', 'Kitchen_ Ceramic / Glazed Tiles Dado', 'Kitchen_ Concealed Plumbing with Premium Quality CP Fitting', 'Kitchen_ Dado Designer Wall Tiles', 'Kitchen_ Designer Tiles Dado up to Door Height', 'Kitchen_ Black Granite Platform', 'Kitchen_ 600mm X 600mm vitrified tiles on floor.', 'Kitchen_ Polished Granite Platform with Stainless Steel Sink', 'Kitchen_ Provision for Water Purifier', 'Kitchen_ 12 x 12 ceramic tiles', 'Kitchen_ Moduler Kitchen with Chimney & HOB', 'Kitchen_ Marble Granite Tiles', 'Kitchen_ Vitrified tiles in kitchen', 'Kitchen_ Reticulated Piped Gas System', 'Kitchen_ C. P. Fittings.', 'Kitchen_ Jaquar / Equivalent CP Fitting', 'Kitchen_ Granite Platform with Stainless Steel Sink and Drain Board', 'Kitchen_ Dado Tiles upto 2 Feet above Platform', 'Kitchen_ Vitrified tile flooring in all rooms', 'Kitchen_ Vitrified tiles flooring', 'Kitchen_ Vitrified tile flooring', 'Kitchen_ Kitchen Virtified Tiles', 'Kitchen_ Italian Modular Cabinets', 'Kitchen_ Anti Skid Tiles', 'Kitchen_ RO System', 'Kitchen_ Piped Gas Connection with Gas Leak Detector', 'Kitchen_ CP Fitting', 'Kitchen_ Vitrify Tiles', 'Kitchen_ Floor Vitrified tile', 'Kitchen_ Glazed tiles dado up to window top', 'Kitchen_ Porcelain Tiles', 'Kitchen_ Designer glazed tile upto full height', 'Kitchen_ Vitrified tiles for flooring', 'Kitchen_ Colour Glazed Tiles Dado', 'Kitchen_ Kitchen 2x2 Vitrified tiles', 'Kitchen_ Vitrified floor tiles', 'Kitchen_ Granite Counter Top with Stainless Steel Sink with Double Bowl', 'Kitchen_ Granite Platform with SS Sink', 'Kitchen_ Dado Tiles', 'Kitchen_ Green Marble', 'Kitchen_ Dishwasher', 'Kitchen_ Granamite Tiles', 'Kitchen_ Standard Fittings', 'Kitchen_ Provision for Water Heater & Water Purifier', 'Kitchen_ Ceramic tiles', 'Kitchen_ Provision For Chimney And Water Purifier', 'Kitchen_ Color Glazed Tiles Dado up to Window Level Height above Platform', 'Kitchen_ Corian Top with Stainless Steel Sink', 'Kitchen_ - Green marble/granite', 'Kitchen_ Modular Kitchen with Stainless Steel Sink', 'Kitchen_ Designer Dado Tiles', 'Kitchen_ Standard Paints', 'Kitchen_ Standard', 'Kitchen_ Marble Platform with SS Sink', 'Kitchen_ Glazed Dado Tiles', 'Kitchen_ Modular Kitchen with Hob & Chimney', 'Kitchen_ Granite Platforms, C.P. & Sanitary Fittings Of Branded Make, Piped Gas System', 'Kitchen_ Provision for Water Purifier & Piped Gas Connection', 'Kitchen_ Vitrified Tiles Dado', 'Kitchen_ Granite Flooring', 'Kitchen_ Marble Top with Sink', 'Kitchen_ Johnson/Vermor Tiles', 'Kitchen_ Indian Marble Counter with Stainless Steel Sink', 'Kitchen_ Ceramic Tiles Dado up to Door Height', 'Kitchen_ Glazed Ceramic Tiles', 'Kitchen_ Ceramic Tiles Dado Till 600 mm above the Counter', 'Kitchen_ Ceramic Tiles up to 600mm Height above the Counter Area', 'Kitchen_ Elegant Vitrified Tiles', 'Kitchen_ Granite Platform', 'Kitchen_ Ceramic Tiles Dado above Working Platform', 'Kitchen_ Aquagaurd', 'Kitchen_ -Anti skid ceramic/vitrified tiled flooring', 'Kitchen_ 2 feet tiles in kitchen above platform', 'Kitchen_', 'Kitchen_ Green Marble Platform with SS Sink', 'Kitchen_ Full marble flooring', 'Kitchen_ Anti Skid Vitrified Tiles', 'Kitchen_ Modular Kitchen with Granite Counter']
        # other_bedroom_am=['Other_Bedroom_ Vitrified Tiles', 'Other_Bedroom_ Vitrified Flooring', 'Other_Bedroom_ 600 rnrn. x 600 rnrn. vitrified tile flooring', 'Other_Bedroom_ Marble Flooring', 'Other_Bedroom_ Vitrified tile flooring', 'Other_Bedroom_ - Vitrified tiles in common bedroom, children bedroom and kitchen', 'Other_Bedroom_ Vitrified tiles', 'Other_Bedroom_ 1mx1m vitrified tiles in bedrooms', 'Other_Bedroom_ Wooden Flooring', 'Other_Bedroom_ Anti Skid Ceramic Tiles', 'Other_Bedroom_ Vitrified Tiled Flooring', 'Other_Bedroom_ Vitrified floor tiles', 'Other_Bedroom_ 2 ft x 2 ft vitrified tile flooring', 'Other_Bedroom_ Laminated Wooden', 'Other_Bedroom_ 600mm x 600mm vitrified tiles in bedrooms', 'Other_Bedroom_ Vitrified tile flooring in bedroom', 'Other_Bedroom_ 2 by 2 vitrified tile flooring in kitchen and bedrooms', 'Other_Bedroom_ Granamite Tiles', 'Other_Bedroom_ Other Bedroom Virtified Tiles', 'Other_Bedroom_ Vitrified tiles in living dinning and bedroom', 'Other_Bedroom_ Vitrified Flooring In Other Bedrooms', 'Other_Bedroom_ Floors Vitrified tiles flooring', 'Other_Bedroom_ Porcelain Tiles', 'Other_Bedroom_ Floor Vitrified Flooring', 'Other_Bedroom_ Ceramic Tiles', 'Other_Bedroom_ Hardwood Flooring', 'Other_Bedroom_ Vitrified tiles in all bedrooms', 'Other_Bedroom_ All Bedrooms Imported engineered wooden flooring', 'Other_Bedroom_ Other Bedroom Vitrified Flooring', 'Other_Bedroom_ Italian Marble', 'Other_Bedroom_ Floors Vitrified tiles 2x2', 'Other_Bedroom_ Vetrified flooring for living, dining and bedrooms', 'Other_Bedroom_ Standard', 'Other_Bedroom_ 800 x 800 vitrified ceramic tiles flooring', 'Other_Bedroom_ Wood Finish Vinyl Flooring', 'Other_Bedroom_ All bedrooms with wooden floorings', 'Other_Bedroom_ Vitrified tiles in bedrooms', 'Other_Bedroom_ Virtified Tiles for Bedroom', 'Other_Bedroom_', 'Other_Bedroom_ Marble Granite Tiles', 'Other_Bedroom_ Vitrified tile flooring.', 'Other_Bedroom_ 2 x 2 vitrified tiles in living, bedroom, dining and kitchen', 'Other_Bedroom_ Vitrified tiles flooring', 'Other_Bedroom_ Marble flooring in all bedrooms']
        # masterbedroom_am=['Master_Bedroom_ Vitrified Tiles', 'Master_Bedroom_ Anti Skid Ceramic Tiles', 'Master_Bedroom_ Vitrified Flooring', 'Master_Bedroom_ Master bedroom Vitrified tiles 600x600', 'Master_Bedroom_ - Master bedroom wooden flooring / other bedrooms vitrified tiles', 'Master_Bedroom_ Marble Flooring', 'Master_Bedroom_ Laminated Wooden Flooring', 'Master_Bedroom_ Wooden flooring', 'Master_Bedroom_ Best Quality Vitrified Tiles', 'Master_Bedroom_ Wodden flooring', 'Master_Bedroom_ Vitrified Tiled Flooring', 'Master_Bedroom_ - Wooden flooring in master bedroom', 'Master_Bedroom_ Laminated Wooden', 'Master_Bedroom_ Wooden Flooring', 'Master_Bedroom_ Vitrify Tiles', 'Master_Bedroom_ Master bedroom 2 x 2 Vitrified tiles', 'Master_Bedroom_ 2 x 2 wooden finish vitrified tiles in Master bedroom', 'Master_Bedroom_ Granamite Tiles', 'Master_Bedroom_ Master Bedroom Vitrified Tile', 'Master_Bedroom_ Vitrified Tiles 2X2', 'Master_Bedroom_ Flooring Vitrified tiles', 'Master_Bedroom_ Vitrified tile flooring.', 'Master_Bedroom_ Porcelain Tiles', 'Master_Bedroom_ Vitrified tiles in all rooms and wooden flooring in master bedroom', 'Master_Bedroom_ Ceramic Tiles', 'Master_Bedroom_ Master Bedrooms Wooden Flooring', 'Master_Bedroom_ Hardwood Flooring', 'Master_Bedroom_ Italian Marble', 'Master_Bedroom_ Wooden finish flooring in master bedroom', 'Master_Bedroom_ Floor Vetrified tiles', 'Master_Bedroom_ Standard', 'Master_Bedroom_ Floor Vitrified tiles', 'Master_Bedroom_ Engineered Wooden Flooring', 'Master_Bedroom_ Master bedroom Vitrified fittings', 'Master_Bedroom_ Wood Finish Vinyl Flooring', 'Master_Bedroom_ Laminated Wooden Floorings', 'Master_Bedroom_ Wooden finish vitrified tiles in master bedroom', 'Master_Bedroom_ 2 x 2 vitrified tiles drawing room , dining room, all bed rooms, kitchen and other area, wooden flooring in master bedroom', 'Master_Bedroom_', 'Master_Bedroom_ Marble Granite Tiles']
        # living_dining_am=['Living_Dining_ Vitrified Tiles', 'Living_Dining_ Anti Skid Tiles', 'Living_Dining_ Marble Flooring', 'Living_Dining_ Vitrified tiles', 'Living_Dining_ Wooden Flooring', 'Living_Dining_ Morbonite Tiles', 'Living_Dining_ Anti Skid Vitrified Tiles', 'Living_Dining_ Marble Granite Tiles', 'Living_Dining_ Imported Marble', 'Living_Dining_ Granamite Tiles', 'Living_Dining_ Porcelain Tiles', 'Living_Dining_ Elegant Vitrified Tiles', 'Living_Dining_ Kota Stone', 'Living_Dining_ Ceramic Tiles', 'Living_Dining_ Italian marble', 'Living_Dining_ Acid Resistant Tiles', 'Living_Dining_ Standard', 'Living_Dining_ Vitrified Flooring', 'Living_Dining_ Johnson/Vermor Tiles', 'Living_Dining_']
        # building_am=['Building_Fire Sprinklers', 'Building_Volleyball Court', 'Building_Community Hall', 'Building_Internal Roads', 'Building_Meter Room', "Building_Children's Play Area", 'Building_Sewage Treatment Plant', 'Building_Yoga/Meditation Area', 'Building_24X7 Water Supply', 'Building_Landscaping & Tree Planting', 'Building_Indoor Games', 'Building_Fire Fighting System', 'Building_Power Backup', 'Building_Entrance Lobby', 'Building_Video Door Security', 'Building_Senior Citizen Siteout', 'Building_Gazebo', 'Building_Water Conservation, Rain water Harvesting', 'Building_Open Parking', 'Building_Community Buildings', 'Building_Car Parking', 'Building_Club House', 'Building_Storm Water Drains', 'Building_Badminton Court', 'Building_Basketball Court', 'Building_Gymnasium', 'Building_Tennis Court', 'Building_Electrification(Transformer, Solar Energy etc)', 'Building_Fire Protection And Fire Safety Requirements', 'Building_Energy management', 'Building_Party Hall', 'Building_Closed Car Parking', 'Building_Open Car Parking', 'Building_Barbecue Area', 'Building_Swimming Pool', 'Building_Multipurpose Hall', 'Building_Carrom', 'Building_Table Tennis', 'Building_Solar Lighting', 'Building_Security Cabin', 'Building_Party Lawn', 'Building_Chess Board', 'Building_Intercom', 'Building_CCTV', 'Building_Solid Waste Management And Disposal', 'Building_Multipurpose Room', 'Building_Rain Water Harvesting', 'Building_Skating Rink', 'Building_Cycling & Jogging Track', 'Building_Internet / Wi-Fi', 'Building_Lift(s)', 'Building_Footpaths/Pedestrian', 'Building_Solar Water Heating', 'Building_Vastu Compliant', 'Building_Waiting Lounge', 'Building_Infinity Pool', 'Building_Rest House for Drivers', 'Building_Partial Power Backup', 'Building_Amphitheater', 'Building_Gated Community', 'Building_24x7 Security', 'Building_Hospital', 'Building_Visitor Parking', 'Building_Temple', "Building_Kid's Pool", 'Building_Banquet Hall', 'Building_Water Storage', 'Building_Reserved Parking', 'Building_Jacuzzi', 'Building_Reflexology Park', 'Building_Bowling Alley', 'Building_Staff Quarter', 'Building_Vaastu Compliant', 'Building_Spa/Sauna/Steam', 'Building_Squash Court', 'Building_Garbage Disposal', 'Building_Paved Compound', 'Building_Card Room', 'Building_Acupressure Center', 'Building_Water Softner Plant', 'Building_Sun Deck', 'Building_Reading Lounge', 'Building_Laundromat', 'Building_Utility Shops', 'Building_Cricket Pitch', 'Building_RO Water System', 'Building_Shopping Mall', 'Building_Valet Parking', 'Building_Service Lift', 'Building_School', 'Building_Recreation Facilities', 'Building_Lift', 'Building_Pool', 'Building_Sports Facility', 'Building_Kids Area', 'Building_Garden', 'Building_Fire Retardant Structure', 'Building_Lawn Tennis Court', 'Building_Pet Grooming', 'Building_Changing Room', 'Building_Salon', 'Building_Mini Theatre', 'Building_Golf Course', 'Building_Bar/Chill-out Lounge', 'Building_Aerobics Room', 'Building_Terrace Garden', 'Building_Open Air Theatre', 'Building_Flower Garden', 'Building_Spa', 'Building_Fountains', 'Building_Business Center', 'Building_Library', 'Building_Earthquake Resistant Structure', 'Building_Steam Room', 'Building_Sauna Bath', 'Building_Health Facilities', 'Building_Restaurants/ Cafeterias', 'Building_Cigar Lounge', 'Building_Multi - Level Parking', 'Building_Billiards/Snooker Table', 'Building_Letter Box', 'Building_Sports Area', 'Building_Maintenance Staff', 'Building_High Speed Elevators', 'Building_Grocery Shop', 'Building_Piped Gas Connection', 'Building_Conference Room', 'Building_Semi Open Car Parking', 'Building_ATM', 'Building_Theme Park', 'Building_Football Field', 'Building_Medical Facilities', 'Building_Medical Store/Pharmacy', 'Building_Doctor on call', 'Building_Pergola', 'Building_Wall Climbing', 'Building_Foosball', 'Building_Business Suites', 'Building_Smoke Detectors', 'Building_Reception/Waiting Room', 'Building_Concierge Service', 'Building_Car Wash Area', 'Building_Security Guards', 'Building_Fire Escape Staircases', 'Building_High-tech alarm system', 'Building_Street Lighting', 'Building_Manicured Garden', 'Building_DG Availability', 'Building_Beach Volley Ball Court', 'Building_Organic Farming', 'Building_Fire Alarm', 'Building_Vertical Garden', 'Building_Gym', 'Building_Water Supply', 'Building_Internal Road', 'Building_Gas Pipeline', 'Building_Bore and Municipal Water', 'Building_Security Guard', 'Building_Food Court', 'Building_Hockey Ground', 'Building_Dart Board', 'Building_Bus Shelter', 'Building_Air Conditioned', 'Building_Boom Barriers', 'Building_Helipad', 'Building_Natural Pond', 'Building_Board Games', 'Building_Water Sports', 'Building_Sports Complex', 'Building_Automated Car Wash', 'Building_Light shows', 'Building_Anti-termite Treatment', 'Building_No Power Backup', 'Building_No Security', 'Building_Sensor operated doors and lifts', 'Building_Sun Bathing', 'Building_Escalators', 'Building_Nature Club', 'Building_Cineplex', 'Building_Grade A Building', 'Building_Central Cooling System', 'Building_Ayurveda Centre', 'Building_Facilities for Disabled', 'Building_Servant Room', 'Building_Full Power Backup', 'Building_Advanced Security', 'Building_Basic Security', 'Building_Bore Water', 'Building_Sub-Station', 'Building_Creche/Day Care', 'Building_Club Rooftop', 'Building_Petrol Pump', 'Building_Lockers', 'Building_Landscaped Garden']

        #### Amenity handle ###

       ##### use this below code for processing
        code_other=[]
        # for i in other_am:
        #   flag=0
        #   op=i.split("_") #4 #16
        #   for va in features[16]:
        #     pat=va
        #     rt=re.findall(pat,op[1],re.I)
        #     if len(rt)>0:
        #       flag=1
        #       break
        #     else:
        #       pass
        #   if flag==1:
        #     code_other.append(1)
        #   else:code_other.append(0)


        coded_exterior=[]
        for i1 in exterior_am:
          flag=0
          op=i1.split("_")
          for va1 in features[3]:
            pat=va1
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_exterior.append(1)
          else:coded_exterior.append(0)

        code_other.extend(coded_exterior)

        coded_interiro=[]
        for i2 in interior_am:
          flag=0
          op=i2.split("_")
          for va2 in features[4]:
            pat=va2
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_interiro.append(1)
          else:coded_interiro.append(0)
        code_other.extend(coded_interiro)

        coded_window=[]
        for i3 in window_am:
          flag=0
          op=i3.split("_")
          for va3 in features[5]:
            pat=va3
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_window.append(1)
          else:coded_window.append(0)

        code_other.extend(coded_window)

        coded_doors=[]
        for i4 in door_am:
          flag=0
          op=i4.split("_")
          for va4 in features[6]:
            pat=va4
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_doors.append(1)
          else:coded_doors.append(0)

        code_other.extend(coded_doors)

        coded_electrical=[]
        for i5 in electrical_am:
          flag=0
          op=i5.split("_")
          for va5 in features[7]:
            pat=va5
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
                print("Electrical Hit",rt)
                flag=1
                break
            else:
                pass
          if flag==1:coded_electrical.append(1)
          else:coded_electrical.append(0)

        code_other.extend(coded_electrical)

        coded_balcony=[]
        for i6 in balcony_am:
          flag=0
          op=i6.split("_")
          for va6 in features[8]:
            pat=va6
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_balcony.append(1)
          else:coded_balcony.append(0)

        code_other.extend(coded_balcony)

        coded_toilet=[]
        for i7 in toilet_am:
          flag=0
          op=i7.split("_")
          for va7 in features[9]:
            pat=va7
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_toilet.append(1)
          else:coded_toilet.append(0)

        code_other.extend(coded_toilet)

        coded_kitchen=[]
        for i8 in kitchen_am:
          flag=0
          op=i8.split("_")
          for va8 in features[10]:
            pat=va8
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_kitchen.append(1)
          else:coded_kitchen.append(0)

        code_other.extend(coded_kitchen)

        coded_other_bed=[]
        for i9 in other_bedroom_am:
          flag=0
          op=i9.split("_")
          for va9 in features[11]:
            pat=va9
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_other_bed.append(1)
          else:coded_other_bed.append(0)

        code_other.extend(coded_other_bed)

        coded_master_b=[]
        for i10 in masterbedroom_am:
          flag=0
          op=i10.split("_")
          for va10 in features[12]:
            pat=va10
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_master_b.append(1)
          else:coded_master_b.append(0)

        code_other.extend(coded_master_b)

        coded_ld=[]
        for i11 in living_dining_am:
          flag=0
          op=i11.split("_")
          for va11 in features[13]:
            pat=va11
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              break
            else:
              pass
          if flag==1:
            coded_ld.append(1)
          else:coded_ld.append(0)
        code_other.extend(coded_ld)


        coded_building=[]
        for i12 in building_am:
          flag=0
          op=i12.split("_")
          for va12 in features[14]:
            pat=va12
            rt=re.findall(pat,op[1],re.I)
            if len(rt)>0:
              flag=1
              print(rt,i12)
              break
            else:
              pass
          if flag==1:
            coded_building.append(1)
          else:coded_building.append(0)

        code_other.extend(coded_building)

        print("LEN OF AMENITY", len(code_other))



        ##### location sorting started #####
        # location=['Ahead of Delhi Public School - Nyati County', 'Ambegaon Budruk', 'Anand Nagar', 'Aundh', 'BT Kawade Road', 'Balewadi', 'Baner', 'Bavdhan', 'Bhoirwadi', 'Bhugaon', 'Bibwewadi', 'Bopodi', 'Central Mumbai Suburbs', 'Chakan', 'Chandan Nagar', 'Charholi Budruk', 'Chikhali', 'Chokhi Dhani', 'Dandekar', 'Dhanori', 'Dhanori Road', 'Dhayri', 'Fursungi', 'Gahunje', 'Ghorpadi', 'Hadapsar', 'Handewadi', 'Hinjewadi', 'Jambhulwadi', 'Kamshet', 'Karegaon', 'Kasarwadi', 'Kesnand', 'Khadakwasla', 'Kharadi', 'Kondhwa', 'Koregaon Park', 'Kothrud', 'Lohegaon', 'Loni Kalbhor', 'Maan', 'Magarpatta City', 'Mahalunge', 'Mamurdi', 'Manjari', 'Mohammadwadi', 'Moshi', 'Mundhwa', 'Nanded', 'Narhe', 'Nasrapur', 'Pashan', 'Pashan Road', 'Paud Road', 'Pimple Nilakh', 'Pimpri Chinchwad', 'Pirangut', 'Porwal Road', 'Punawale', 'Pune', 'Pune Cantonment', 'Rahatani', 'Ranjangaon', 'Ravet', 'Sanaswadi', 'Shaniwar Peth', 'Sinhagad Road', 'Sus', 'Talegaon Dabhade', 'Talegaon Dhamdhere', 'Tathawade', 'Undri', 'Vadgaon Budruk', 'Viman Nagar', 'Wadgaon Sheri', 'Wagholi', 'Wakad', 'Wanowrie', 'Wanwadi']

        coded_location=[]
        for indl,vall in enumerate(location):
            if event['location'].lower() in vall.lower():
                coded_location.append(1)
            else:
                coded_location.append(0)
        print("LOCATIOOOOOO",len(coded_location))
        #### other GIS feature started ####


        gis_coded=[]
        for col,row in gi_da.iterrows():
          if event['location'].lower() in row['Location'].lower():
            for i in gis_feat:
              # print(row[f'{i}'])
              gis_coded.append(row[f'{i}'])
            break
        print("GIOS",len(gis_coded))

        final_val.extend(gis_coded)
        # final_val.extend(gis_listy)
        final_val.extend(code_other)
        final_val.extend(coded_location)
        # final_val.append(pr)

        print("FINALL LENGHT ",len(final_val))


        lp =[]
        for ko in final_val:
            try:
                lp.append(float(ko))
            except:
                print(ko)

        print(lp)



        # ss=['Area', 'BHK', 'Bathroom', 'Balcony', 'Best_Gas_station_count', 'Best_Shopping_mall_count', 'Best_school_count', 'Best_Restaurant_count', 'Best_ATM_count', 'Best_Hospital_count', 'ATM_count', 'Gas_station_count', 'Shopping_mall_count', 'School_count', 'Hospital_count', 'Restaurant_count', 'Others_Others', 'Others_ Standard', 'Others_ Standard Fittings', 'Others_', 'Exterior_ Acrylic Paint', 'Exterior_ Asian Paint', 'Exterior_ Paint, Distemper', 'Exterior_ Sand Faced Plaster', 'Exterior_ Texture Paint', 'Exterior_ Apex Paint', 'Exterior_ Weather proof paint', 'Exterior_ Acrylic Emulsion Paint', 'Exterior_ Gypsum Finish', 'Exterior_ Apex Weatherproof Emulsion Paint', 'Exterior_ Emulsion Paint', 'Exterior_ Superior quality cement paint for external walls and oil bound for internal walls', 'Exterior_ Good Quality Paint', 'Exterior_ Oil Bound Distemper Paint', 'Exterior_ Semi Acrylic Paint', 'Exterior_ ACE Paint', 'Exterior_ Weather Proof Paint', 'Exterior_ Water Resistant Paint', 'Exterior_ Exterior Paint', 'Exterior_ High Quality Texture Paint', 'Exterior_ Cement Paint', 'Exterior_ Plastic Paint', 'Exterior_ Cement Based Paint', 'Exterior_ POP Finish', 'Exterior_ Exterior Grade Acrylic Emulsion', 'Exterior_ Acrylic Paints', 'Exterior_ Plastic Emulsion Paint', 'Exterior_ Water Proof Cement Paint', 'Exterior_ Standard Paints', 'Exterior_ Texture Paints', 'Exterior_ Weather Coat Paint', 'Exterior_ Superior Paint Finish', 'Exterior_ Plastic Paints', 'Exterior_', 'Exterior_ Weather Proof Texture Paint', 'Exterior_ Sandfaced Paints', 'Exterior_ Oil Bound Distemper', 'Interior_ Oil Bound Distemper', 'Interior_ Putty on Walls', 'Interior_ Acrylic Paint', 'Interior_ Gypsum Finish', 'Interior_ Plaster & OBD', 'Interior_ Plastic Paint', 'Interior_ Emulsion Paint', 'Interior_ Acrylic Emulsion Paint', 'Interior_ Plastic Emulsion Paint', 'Interior_ Texture Paint', 'Interior_ Acrylic Emulsion Paint with Putty', 'Interior_ ACE Paint', 'Interior_ POP Finish', 'Interior_ Luster Paint', 'Interior_ Paint, Distemper', 'Interior_ Sand Faced Plaster', 'Interior_ POP Punning with OBD Finish', 'Interior_ Cement Based Paint', 'Interior_ Semi Acrylic Paint', 'Interior_ Asian Paint', 'Interior_ Good Quality Paint', 'Interior_ OBD Paints', 'Interior_ Acrylic Emulsion Paints', 'Interior_ Acrylic OBD Paints', 'Interior_ Plastic Emulsion Paints', 'Interior_ Oil Bound Paints', 'Interior_ OBD', 'Interior_ Luster Paint and Plastic Paint', 'Interior_ Standard Paints', 'Interior_ Standard Paint', 'Interior_ Acrylic Emulsion Paint on POP Punning', 'Interior_', 'Interior_ Gypsum Paints', 'Windows_ Powder Coated Aluminium Sliding Window', 'Windows_ 3 Track Powder Coated Aluminium Windows', 'Windows_ Aluminium Powder Coated Windows', 'Windows_ Powder Coated Aluminium Sliding', 'Windows_ 3 Track UPVC Windows with SS Mosquito Net', 'Windows_ UPVC Sliding Windows', 'Windows_ Aluminium Sliding Windows', 'Windows_ Aluminium Powder Coated Windows With Mosquito Mesh', 'Windows_ Anodized Aluminium Sliding with M.S Grill', 'Windows_ Aluminium Powder Coated Glazed Windows', 'Windows_ Aluminium Powder Coated 3-Track Sliding with Reflective Glass', 'Windows_ Anodized Aluminium Sliding', 'Windows_ Aluminium / UPVC / HardWood', 'Windows_ Powder coated aluminium sliding windows', 'Windows_ Powder Coated / Anodized Aluminium Sliding Windows', 'Windows_ Aluminium Frames with Glazed Shutters', 'Windows_ Powder coated aluminum sliding windows with safety grills and window sills', 'Windows_ Powder Coated Aluminum / UPVC Frames', 'Windows_ UPVC windows', 'Windows_ Aluminium Sliding', 'Windows_ Aluminium windows', 'Windows_ High Quality Aluminium Sliding Windows', 'Windows_ UPVC Windows with Granite Sills', 'Windows_ 2 Track UPVC Sliding Window with Mosquito Mesh Shutter', 'Windows_ Powder coated aluminium windows', 'Windows_ Anodised aluminium windows with mosquito nets', 'Windows_ Anodized aluminium windows', 'Windows_ Powder Coated Aluminium Sliding Windows', 'Windows_ Anodised / Powder Coated Aluminium Sliding Windows', 'Windows_ Powder Coated Aluminium Glazing', 'Windows_ Anodised Aluminium Window with MS Safety Grill & Mosquito Mesh', 'Windows_ Powder Coated Aluminium Sliding Windows with Mosquito Nets', 'Windows_ Standard Fittings', 'Windows_ Powder Coated Windows with Grills', 'Windows_ Powder Coated Aluminium Sliding Window With Mosquito Mesh, M.S. Safety Grill For Windows', 'Windows_ Standard', 'Windows_ M.S. Frame and Flush Door Shutter', 'Windows_ Anodized / Powder Coated Glazed Aluminium', 'Windows_ UPVC / Aluminium Windows', 'Windows_ Standard Windows', 'Windows_', 'Windows_ Aluminum Sliding Window with Mosquito Mesh Shutters', 'Windows_ Powder Coated Aluminium Windows', 'Windows_ French Windows', 'Doors_ Decorative Laminated Door', 'Doors_ Laminated Flush Door', 'Doors_ Decorative Main Door', 'Doors_ Aluminium/UPVC Doors', 'Doors_ Hard Wood Frame', 'Doors_ Veneered Door', 'Doors_ Both Side Laminated Flush Door', 'Doors_ Moulded Designer Door', 'Doors_ Designer Door', 'Doors_ Decorative Flush Door', 'Doors_ Decorative with Wooden Frame', 'Doors_ Wooden Frame', 'Doors_ Elegant Door', 'Doors_ Wooden Door with Teak Wood Finish', 'Doors_ Teak Wood Doors', 'Doors_ Decorative Door with Quality Brass Fittings Safety Lock', 'Doors_ Flush Door', 'Doors_ Decorative Laminate', 'Doors_ Pre Engineered Steel Frame with Wooden Shutters', 'Doors_ Decorative with Brass Fittings', 'Doors_ Veneer Flush Doors', 'Doors_ Teak Veneered / Laminated Flush Door', 'Doors_ Aluminium with Wooden Shade', 'Doors_ Wood Frame', 'Doors_ Verneer Finish Main Door', 'Doors_ Laminated Frame Doors', 'Doors_ Wooden Doors', 'Doors_ Moulded Skin Doors', 'Doors_ Teak Wood Frame', 'Doors_ Decorative Wooden Frame Door', 'Doors_ Standards Quality Doors', 'Doors_ Heavy Duty Wooden Laminated Doors', 'Doors_ Standard Fittings', 'Doors_ Laminated Doors', 'Doors_ Laminate On Both Sides With Branded Locks', 'Doors_ Laminated Flush Doors', 'Doors_ Standard', 'Doors_ Moduled Doors', 'Doors_ Decorative Flush with Hardwood Door Frames', 'Doors_ Beach Wood Frame', 'Doors_', 'Doors_ Teak Wood Frame and Shutter', 'Doors_ Decorativ Door', 'Doors_ Wooden Fittings', 'Electrical_ Concealed copper wiring', 'Electrical_ Concealed Copper Wiring with Adequate Points', 'Electrical_ Concealed Copper Wiring with Circuit Breakers', 'Electrical_ Concealed Fire Resistant Copper Wiring', 'Electrical_ Concealed Copper Wiring with MCB/ ELCB', 'Electrical_ Copper Wiring in PVC Concealed Conduit', 'Electrical_ Concealed Copper Wiring', 'Electrical_ Havells/Anchor Make', 'Electrical_ Standard', 'Electrical_ ISI Copper Wiring in PVC Concealed Conduit', 'Electrical_ Finolex or Equivalent Cables and Wiring', 'Electrical_ Concealed Copper Electric Wiring with Essential Points', 'Electrical_ Concealed Copper Wirings', 'Electrical_ Standard Fittings', 'Electrical_ Branded Concealed Copper Wiring with MCB / ELCB', 'Electrical_ Concealed Copper Wirings with Modular Switches', 'Electrical_ Legrand / Equivalent Electrical Switches', 'Electrical_ Electrical Switches Of Branded Make', 'Electrical_', 'Electrical_ Concealed Wirings with Modular Switches', 'Balcony_ Anti Skid Tiles', 'Balcony_ Ceramic Tiles', 'Balcony_ Vitrified Tiles', 'Balcony_ Anti skid ceramic tiles', 'Balcony_ Designer Tiles', 'Balcony_ Anti Skid Vitrified Tiles', 'Balcony_ Rustic Tiles', 'Balcony_ Marble Granite Tiles', 'Balcony_ Italian Marble', 'Balcony_ Standard', 'Balcony_ Anti-Skid Flooring', 'Balcony_ Johnson/Vermor Tiles', 'Balcony_ Wooden Flooring', 'Balcony_', 'Balcony_ Standard Floorings', 'Toilets_ Anti Skid Tiles', 'Toilets_ CP Fittings of Jaquar / Marc or Equivalent', 'Toilets_ Designer Tiles Dado', 'Toilets_ Designer Bath Fittings', 'Toilets_ Anti Skid Ceramic Tiles', 'Toilets_ Branded CP Fittings & Sanitary Ware, Anti-Skid Tiles', 'Toilets_ Ceramic Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Ceramic Tiles', 'Toilets_ Ceramic Tiles and Border', 'Toilets_ Branded CP Fittings and Sanitary Ware', 'Toilets_ Ceramic Tiles Dado', 'Toilets_ Vitrified Tiles', 'Toilets_ Provision For Exhaust Fan', 'Toilets_ Anti Skid Tiles Dado', 'Toilets_ CP fittings', 'Toilets_ Sanitary fittings', 'Toilets_ Vitrified / Ceramic Tiles Dado', 'Toilets_ Branded CP Fitting', 'Toilets_ Designer Tiles Dado up to Lintel Level', 'Toilets_ Kohler/Roca/American Standard or Equivalent Make', 'Toilets_ Ceramic Tiles Dado up to Lintel Level', 'Toilets_ Glazed Tiles Dado', 'Toilets_ Branded Sanitary Fittings', 'Toilets_ Tile Dado up to 7 Feet/Lintel Height.', 'Toilets_ CP Fittings from Essco or Equivalent Make', 'Toilets_ Glazed Tiles Dado up to Lintel Level', 'Toilets_ Branded CP Fittings with Hot & Cold Mixer', 'Toilets_ Designer Tiles Dado up to Door Height', 'Toilets_ GI / CPVC / PPR Pipes', 'Toilets_ Anti Skid Vitrified Tiles', 'Toilets_ Good Quality CP Fittings of Jaquar or Equivalent', 'Toilets_ Designer Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Premium CP Fittings', 'Toilets_ Hindware / Parryware or Equivalent Sanitary Fittings', 'Toilets_ Sanitary Ware / Parryware / Hindware or Equivalent Sanitary Fittings', 'Toilets_ Matt Finish Tiles', 'Toilets_ Single Lever CP Brass Fittings', 'Toilets_ Premium Sanitary Fittings', 'Toilets_ Provision for exhaust fan and anti-skid flooring', 'Toilets_ Concealed plumbing with premium quality CF fittings', 'Toilets_ Hot and Cold Water Mixer', 'Toilets_ Marble Granite Tiles', 'Toilets_ Full Height Designer Tiles', 'Toilets_ Provision for Wash Basin', 'Toilets_ ISI Branded Chromium Plated Tap', 'Toilets_ Chrome Plated Fittings', 'Toilets_ Glazed Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Parryware or Equivalent Sanitary Fittings', 'Toilets_ European Water Closet', 'Toilets_ Provision for Geyser', 'Toilets_ Dado of Glazed /Ceramic Tiles', 'Toilets_ Wash Basin', 'Toilets_ Concealed Plumbing', 'Toilets_ Concealed Plumbing with Hot & Cold Mixer', 'Toilets_ Ant Skid Ceramic Tiles', 'Toilets_ Jaguar Fittings', 'Toilets_ Designer Tiles on Dado upto Door Height', 'Toilets_ Cera / Equivalent Sanitary Fittings', 'Toilets_ Superior Quality Ceramic Tiles up to False Ceiling', 'Toilets_ Glazed Tiles', 'Toilets_ Vitrified Tiles (Kajaria)', 'Toilets_ High Quality CP Fittings', 'Toilets_ CP Fittings', 'Toilets_ Dado Tiles', 'Toilets_ Standard Fittings', 'Toilets_ Sanitary ware of Parry ware or equivalent', 'Toilets_ Sanitary Fittings', 'Toilets_ Branded Bathroom Fittings', 'Toilets_ Italian Marble', 'Toilets_ Acid Resistant Tiles', 'Toilets_ Standard Paints', 'Toilets_ EWC', 'Toilets_ Glazed Tiles Dado Up to Door Height', 'Toilets_ Ceramic Dado Tiles', 'Toilets_ Standard', 'Toilets_ Glazed Dado Tiles', 'Toilets_ Granite Counter', 'Toilets_ Toto / Equivalent Bathroom Fittings', 'Toilets_ Anti-Skid Flooring', 'Toilets_ Provision For Exhaust In Bathrooms, C.P. & Sanitary Fittings Of Branded Make, Glass Divider In Master Bathroom', 'Toilets_ Marble Flooring', 'Toilets_ Imported Marble Dado', 'Toilets_ Imported Marble', 'Toilets_ Full Height Tiles', 'Toilets_ Johnson/Vermor Tiles', 'Toilets_ Glazed Ceramic Tiles', 'Toilets_ Mirror', 'Toilets_ Combination of Ceramic/Vitrified Tiles Dado', 'Toilets_', 'Toilets_ Provision for Solar System', 'Toilets_ Designer Dado Tiles', 'Kitchen_ Vitrified Tiles', 'Kitchen_ Exhaust Fan', 'Kitchen_ Glazed Tiles Dado', 'Kitchen_ Granite platform with stainless steel sink', 'Kitchen_ Provision For Water Purifier and Exhaust Fan', 'Kitchen_ Ceramic Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ - Granite counter in kitchen area', 'Kitchen_ Anti Skid Tiles Dado', 'Kitchen_ Designer Tiles Dado', 'Kitchen_ Vitrified Flooring', 'Kitchen_ Modular Kitchen', 'Kitchen_ Stainless Steel Sink', 'Kitchen_ Ceramic Tiles Dado', 'Kitchen_ Ceramic tiles dado upto lintel level', 'Kitchen_ Italian Marble', 'Kitchen_ Designer Tiles Dado up to Lintel Level', 'Kitchen_ Branded CP fittings', 'Kitchen_ Ceramic Tiles Dado up to Lintel Level', 'Kitchen_ Vetrified tile flooring', 'Kitchen_ Almirah / Cabinet (No HOB & CHIMNEY)', 'Kitchen_ Designer Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ Glazed Tiles above Platform', 'Kitchen_ Marble Flooring', 'Kitchen_ Vitrified tiles on floor', 'Kitchen_ Tiles Dado up to Beam Level over Platform', 'Kitchen_ Chimney', 'Kitchen_ Ceramic Tiles', 'Kitchen_ Glazed Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ Granite Platform with Stainless Steel Sink', 'Kitchen_ Granite platform', 'Kitchen_ - Vitrified flooring', 'Kitchen_ Double bowl stainless steel sink', 'Kitchen_ Glazed Tiles Dado up to Lintel Level', 'Kitchen_ Ceramic / Glazed Tiles Dado', 'Kitchen_ Concealed Plumbing with Premium Quality CP Fitting', 'Kitchen_ Dado Designer Wall Tiles', 'Kitchen_ Designer Tiles Dado up to Door Height', 'Kitchen_ Black Granite Platform', 'Kitchen_ 600mm X 600mm vitrified tiles on floor.', 'Kitchen_ Polished Granite Platform with Stainless Steel Sink', 'Kitchen_ Provision for Water Purifier', 'Kitchen_ 12 x 12 ceramic tiles', 'Kitchen_ Moduler Kitchen with Chimney & HOB', 'Kitchen_ Marble Granite Tiles', 'Kitchen_ Vitrified tiles in kitchen', 'Kitchen_ Reticulated Piped Gas System', 'Kitchen_ C. P. Fittings.', 'Kitchen_ Jaquar / Equivalent CP Fitting', 'Kitchen_ Granite Platform with Stainless Steel Sink and Drain Board', 'Kitchen_ Dado Tiles upto 2 Feet above Platform', 'Kitchen_ Vitrified tile flooring in all rooms', 'Kitchen_ Vitrified tiles flooring', 'Kitchen_ Vitrified tile flooring', 'Kitchen_ Kitchen Virtified Tiles', 'Kitchen_ Italian Modular Cabinets', 'Kitchen_ Anti Skid Tiles', 'Kitchen_ RO System', 'Kitchen_ Piped Gas Connection with Gas Leak Detector', 'Kitchen_ CP Fitting', 'Kitchen_ Vitrify Tiles', 'Kitchen_ Floor Vitrified tile', 'Kitchen_ Glazed tiles dado up to window top', 'Kitchen_ Porcelain Tiles', 'Kitchen_ Designer glazed tile upto full height', 'Kitchen_ Vitrified tiles for flooring', 'Kitchen_ Colour Glazed Tiles Dado', 'Kitchen_ Kitchen 2x2 Vitrified tiles', 'Kitchen_ Vitrified floor tiles', 'Kitchen_ Granite Counter Top with Stainless Steel Sink with Double Bowl', 'Kitchen_ Granite Platform with SS Sink', 'Kitchen_ Dado Tiles', 'Kitchen_ Green Marble', 'Kitchen_ Dishwasher', 'Kitchen_ Granamite Tiles', 'Kitchen_ Standard Fittings', 'Kitchen_ Provision for Water Heater & Water Purifier', 'Kitchen_ Ceramic tiles', 'Kitchen_ Provision For Chimney And Water Purifier', 'Kitchen_ Color Glazed Tiles Dado up to Window Level Height above Platform', 'Kitchen_ Corian Top with Stainless Steel Sink', 'Kitchen_ - Green marble/granite', 'Kitchen_ Modular Kitchen with Stainless Steel Sink', 'Kitchen_ Designer Dado Tiles', 'Kitchen_ Standard Paints', 'Kitchen_ Standard', 'Kitchen_ Marble Platform with SS Sink', 'Kitchen_ Glazed Dado Tiles', 'Kitchen_ Modular Kitchen with Hob & Chimney', 'Kitchen_ Granite Platforms, C.P. & Sanitary Fittings Of Branded Make, Piped Gas System', 'Kitchen_ Provision for Water Purifier & Piped Gas Connection', 'Kitchen_ Vitrified Tiles Dado', 'Kitchen_ Granite Flooring', 'Kitchen_ Marble Top with Sink', 'Kitchen_ Johnson/Vermor Tiles', 'Kitchen_ Indian Marble Counter with Stainless Steel Sink', 'Kitchen_ Ceramic Tiles Dado up to Door Height', 'Kitchen_ Glazed Ceramic Tiles', 'Kitchen_ Ceramic Tiles Dado Till 600 mm above the Counter', 'Kitchen_ Ceramic Tiles up to 600mm Height above the Counter Area', 'Kitchen_ Elegant Vitrified Tiles', 'Kitchen_ Granite Platform', 'Kitchen_ Ceramic Tiles Dado above Working Platform', 'Kitchen_ Aquagaurd', 'Kitchen_ -Anti skid ceramic/vitrified tiled flooring', 'Kitchen_ 2 feet tiles in kitchen above platform', 'Kitchen_', 'Kitchen_ Green Marble Platform with SS Sink', 'Kitchen_ Full marble flooring', 'Kitchen_ Anti Skid Vitrified Tiles', 'Kitchen_ Modular Kitchen with Granite Counter', 'Other_Bedroom_ Vitrified Tiles', 'Other_Bedroom_ Vitrified Flooring', 'Other_Bedroom_ 600 rnrn. x 600 rnrn. vitrified tile flooring', 'Other_Bedroom_ Marble Flooring', 'Other_Bedroom_ Vitrified tile flooring', 'Other_Bedroom_ - Vitrified tiles in common bedroom, children bedroom and kitchen', 'Other_Bedroom_ Vitrified tiles', 'Other_Bedroom_ 1mx1m vitrified tiles in bedrooms', 'Other_Bedroom_ Wooden Flooring', 'Other_Bedroom_ Anti Skid Ceramic Tiles', 'Other_Bedroom_ Vitrified Tiled Flooring', 'Other_Bedroom_ Vitrified floor tiles', 'Other_Bedroom_ 2 ft x 2 ft vitrified tile flooring', 'Other_Bedroom_ Laminated Wooden', 'Other_Bedroom_ 600mm x 600mm vitrified tiles in bedrooms', 'Other_Bedroom_ Vitrified tile flooring in bedroom', 'Other_Bedroom_ 2 by 2 vitrified tile flooring in kitchen and bedrooms', 'Other_Bedroom_ Granamite Tiles', 'Other_Bedroom_ Other Bedroom Virtified Tiles', 'Other_Bedroom_ Vitrified tiles in living dinning and bedroom', 'Other_Bedroom_ Vitrified Flooring In Other Bedrooms', 'Other_Bedroom_ Floors Vitrified tiles flooring', 'Other_Bedroom_ Porcelain Tiles', 'Other_Bedroom_ Floor Vitrified Flooring', 'Other_Bedroom_ Ceramic Tiles', 'Other_Bedroom_ Hardwood Flooring', 'Other_Bedroom_ Vitrified tiles in all bedrooms', 'Other_Bedroom_ All Bedrooms Imported engineered wooden flooring', 'Other_Bedroom_ Other Bedroom Vitrified Flooring', 'Other_Bedroom_ Italian Marble', 'Other_Bedroom_ Floors Vitrified tiles 2x2', 'Other_Bedroom_ Vetrified flooring for living, dining and bedrooms', 'Other_Bedroom_ Standard', 'Other_Bedroom_ 800 x 800 vitrified ceramic tiles flooring', 'Other_Bedroom_ Wood Finish Vinyl Flooring', 'Other_Bedroom_ All bedrooms with wooden floorings', 'Other_Bedroom_ Vitrified tiles in bedrooms', 'Other_Bedroom_ Virtified Tiles for Bedroom', 'Other_Bedroom_', 'Other_Bedroom_ Marble Granite Tiles', 'Other_Bedroom_ Vitrified tile flooring.', 'Other_Bedroom_ 2 x 2 vitrified tiles in living, bedroom, dining and kitchen', 'Other_Bedroom_ Vitrified tiles flooring', 'Other_Bedroom_ Marble flooring in all bedrooms', 'Master_Bedroom_ Vitrified Tiles', 'Master_Bedroom_ Anti Skid Ceramic Tiles', 'Master_Bedroom_ Vitrified Flooring', 'Master_Bedroom_ Master bedroom Vitrified tiles 600x600', 'Master_Bedroom_ - Master bedroom wooden flooring / other bedrooms vitrified tiles', 'Master_Bedroom_ Marble Flooring', 'Master_Bedroom_ Laminated Wooden Flooring', 'Master_Bedroom_ Wooden flooring', 'Master_Bedroom_ Best Quality Vitrified Tiles', 'Master_Bedroom_ Wodden flooring', 'Master_Bedroom_ Vitrified Tiled Flooring', 'Master_Bedroom_ - Wooden flooring in master bedroom', 'Master_Bedroom_ Laminated Wooden', 'Master_Bedroom_ Wooden Flooring', 'Master_Bedroom_ Vitrify Tiles', 'Master_Bedroom_ Master bedroom 2 x 2 Vitrified tiles', 'Master_Bedroom_ 2 x 2 wooden finish vitrified tiles in Master bedroom', 'Master_Bedroom_ Granamite Tiles', 'Master_Bedroom_ Master Bedroom Vitrified Tile', 'Master_Bedroom_ Vitrified Tiles 2X2', 'Master_Bedroom_ Flooring Vitrified tiles', 'Master_Bedroom_ Vitrified tile flooring.', 'Master_Bedroom_ Porcelain Tiles', 'Master_Bedroom_ Vitrified tiles in all rooms and wooden flooring in master bedroom', 'Master_Bedroom_ Ceramic Tiles', 'Master_Bedroom_ Master Bedrooms Wooden Flooring', 'Master_Bedroom_ Hardwood Flooring', 'Master_Bedroom_ Italian Marble', 'Master_Bedroom_ Wooden finish flooring in master bedroom', 'Master_Bedroom_ Floor Vetrified tiles', 'Master_Bedroom_ Standard', 'Master_Bedroom_ Floor Vitrified tiles', 'Master_Bedroom_ Engineered Wooden Flooring', 'Master_Bedroom_ Master bedroom Vitrified fittings', 'Master_Bedroom_ Wood Finish Vinyl Flooring', 'Master_Bedroom_ Laminated Wooden Floorings', 'Master_Bedroom_ Wooden finish vitrified tiles in master bedroom', 'Master_Bedroom_ 2 x 2 vitrified tiles drawing room , dining room, all bed rooms, kitchen and other area, wooden flooring in master bedroom', 'Master_Bedroom_', 'Master_Bedroom_ Marble Granite Tiles', 'Living_Dining_ Vitrified Tiles', 'Living_Dining_ Anti Skid Tiles', 'Living_Dining_ Marble Flooring', 'Living_Dining_ Vitrified tiles', 'Living_Dining_ Wooden Flooring', 'Living_Dining_ Morbonite Tiles', 'Living_Dining_ Anti Skid Vitrified Tiles', 'Living_Dining_ Marble Granite Tiles', 'Living_Dining_ Imported Marble', 'Living_Dining_ Granamite Tiles', 'Living_Dining_ Porcelain Tiles', 'Living_Dining_ Elegant Vitrified Tiles', 'Living_Dining_ Kota Stone', 'Living_Dining_ Ceramic Tiles', 'Living_Dining_ Italian marble', 'Living_Dining_ Acid Resistant Tiles', 'Living_Dining_ Standard', 'Living_Dining_ Vitrified Flooring', 'Living_Dining_ Johnson/Vermor Tiles', 'Living_Dining_', 'Building_Fire Sprinklers', 'Building_Volleyball Court', 'Building_Community Hall', 'Building_Internal Roads', 'Building_Meter Room', "Building_Children's Play Area", 'Building_Sewage Treatment Plant', 'Building_Yoga/Meditation Area', 'Building_24X7 Water Supply', 'Building_Landscaping & Tree Planting', 'Building_Indoor Games', 'Building_Fire Fighting System', 'Building_Power Backup', 'Building_Entrance Lobby', 'Building_Video Door Security', 'Building_Senior Citizen Siteout', 'Building_Gazebo', 'Building_Water Conservation, Rain water Harvesting', 'Building_Open Parking', 'Building_Community Buildings', 'Building_Car Parking', 'Building_Club House', 'Building_Storm Water Drains', 'Building_Badminton Court', 'Building_Basketball Court', 'Building_Gymnasium', 'Building_Tennis Court', 'Building_Electrification(Transformer, Solar Energy etc)', 'Building_Fire Protection And Fire Safety Requirements', 'Building_Energy management', 'Building_Party Hall', 'Building_Closed Car Parking', 'Building_Open Car Parking', 'Building_Barbecue Area', 'Building_Swimming Pool', 'Building_Multipurpose Hall', 'Building_Carrom', 'Building_Table Tennis', 'Building_Solar Lighting', 'Building_Security Cabin', 'Building_Party Lawn', 'Building_Chess Board', 'Building_Intercom', 'Building_CCTV', 'Building_Solid Waste Management And Disposal', 'Building_Multipurpose Room', 'Building_Rain Water Harvesting', 'Building_Skating Rink', 'Building_Cycling & Jogging Track', 'Building_Internet / Wi-Fi', 'Building_Lift(s)', 'Building_Footpaths/Pedestrian', 'Building_Solar Water Heating', 'Building_Vastu Compliant', 'Building_Waiting Lounge', 'Building_Infinity Pool', 'Building_Rest House for Drivers', 'Building_Partial Power Backup', 'Building_Amphitheater', 'Building_Gated Community', 'Building_24x7 Security', 'Building_Hospital', 'Building_Visitor Parking', 'Building_Temple', "Building_Kid's Pool", 'Building_Banquet Hall', 'Building_Water Storage', 'Building_Reserved Parking', 'Building_Jacuzzi', 'Building_Reflexology Park', 'Building_Bowling Alley', 'Building_Staff Quarter', 'Building_Vaastu Compliant', 'Building_Spa/Sauna/Steam', 'Building_Squash Court', 'Building_Garbage Disposal', 'Building_Paved Compound', 'Building_Card Room', 'Building_Acupressure Center', 'Building_Water Softner Plant', 'Building_Sun Deck', 'Building_Reading Lounge', 'Building_Laundromat', 'Building_Utility Shops', 'Building_Cricket Pitch', 'Building_RO Water System', 'Building_Shopping Mall', 'Building_Valet Parking', 'Building_Service Lift', 'Building_School', 'Building_Recreation Facilities', 'Building_Lift', 'Building_Pool', 'Building_Sports Facility', 'Building_Kids Area', 'Building_Garden', 'Building_Fire Retardant Structure', 'Building_Lawn Tennis Court', 'Building_Pet Grooming', 'Building_Changing Room', 'Building_Salon', 'Building_Mini Theatre', 'Building_Golf Course', 'Building_Bar/Chill-out Lounge', 'Building_Aerobics Room', 'Building_Terrace Garden', 'Building_Open Air Theatre', 'Building_Flower Garden', 'Building_Spa', 'Building_Fountains', 'Building_Business Center', 'Building_Library', 'Building_Earthquake Resistant Structure', 'Building_Steam Room', 'Building_Sauna Bath', 'Building_Health Facilities', 'Building_Restaurants/ Cafeterias', 'Building_Cigar Lounge', 'Building_Multi - Level Parking', 'Building_Billiards/Snooker Table', 'Building_Letter Box', 'Building_Sports Area', 'Building_Maintenance Staff', 'Building_High Speed Elevators', 'Building_Grocery Shop', 'Building_Piped Gas Connection', 'Building_Conference Room', 'Building_Semi Open Car Parking', 'Building_ATM', 'Building_Theme Park', 'Building_Football Field', 'Building_Medical Facilities', 'Building_Medical Store/Pharmacy', 'Building_Doctor on call', 'Building_Pergola', 'Building_Wall Climbing', 'Building_Foosball', 'Building_Business Suites', 'Building_Smoke Detectors', 'Building_Reception/Waiting Room', 'Building_Concierge Service', 'Building_Car Wash Area', 'Building_Security Guards', 'Building_Fire Escape Staircases', 'Building_High-tech alarm system', 'Building_Street Lighting', 'Building_Manicured Garden', 'Building_DG Availability', 'Building_Beach Volley Ball Court', 'Building_Organic Farming', 'Building_Fire Alarm', 'Building_Vertical Garden', 'Building_Gym', 'Building_Water Supply', 'Building_Internal Road', 'Building_Gas Pipeline', 'Building_Bore and Municipal Water', 'Building_Security Guard', 'Building_Food Court', 'Building_Hockey Ground', 'Building_Dart Board', 'Building_Bus Shelter', 'Building_Air Conditioned', 'Building_Boom Barriers', 'Building_Helipad', 'Building_Natural Pond', 'Building_Board Games', 'Building_Water Sports', 'Building_Sports Complex', 'Building_Automated Car Wash', 'Building_Light shows', 'Building_Anti-termite Treatment', 'Building_No Power Backup', 'Building_No Security', 'Building_Sensor operated doors and lifts', 'Building_Sun Bathing', 'Building_Escalators', 'Building_Nature Club', 'Building_Cineplex', 'Building_Grade A Building', 'Building_Central Cooling System', 'Building_Ayurveda Centre', 'Building_Facilities for Disabled', 'Building_Servant Room', 'Building_Full Power Backup', 'Building_Advanced Security', 'Building_Basic Security', 'Building_Bore Water', 'Building_Sub-Station', 'Building_Creche/Day Care', 'Building_Club Rooftop', 'Building_Petrol Pump', 'Building_Lockers', 'Building_Landscaped Garden', 'Ahead of Delhi Public School - Nyati County', 'Ambegaon Budruk', 'Anand Nagar', 'Aundh', 'BT Kawade Road', 'Balewadi', 'Baner', 'Bavdhan', 'Bhoirwadi', 'Bhugaon', 'Bibwewadi', 'Bopodi', 'Central Mumbai Suburbs', 'Chakan', 'Chandan Nagar', 'Charholi Budruk', 'Chikhali', 'Chokhi Dhani', 'Dandekar', 'Dhanori', 'Dhanori Road', 'Dhayri', 'Fursungi', 'Gahunje', 'Ghorpadi', 'Hadapsar', 'Handewadi', 'Hinjewadi', 'Jambhulwadi', 'Kamshet', 'Karegaon', 'Kasarwadi', 'Kesnand', 'Khadakwasla', 'Kharadi', 'Kondhwa', 'Koregaon Park', 'Kothrud', 'Lohegaon', 'Loni Kalbhor', 'Maan', 'Magarpatta City', 'Mahalunge', 'Mamurdi', 'Manjari', 'Mohammadwadi', 'Moshi', 'Mundhwa', 'Nanded', 'Narhe', 'Nasrapur', 'Pashan', 'Pashan Road', 'Paud Road', 'Pimple Nilakh', 'Pimpri Chinchwad', 'Pirangut', 'Porwal Road', 'Punawale', 'Pune', 'Pune Cantonment', 'Rahatani', 'Ranjangaon', 'Ravet', 'Sanaswadi', 'Shaniwar Peth', 'Sinhagad Road', 'Sus', 'Talegaon Dabhade', 'Talegaon Dhamdhere', 'Tathawade', 'Undri', 'Vadgaon Budruk', 'Viman Nagar', 'Wadgaon Sheri', 'Wagholi', 'Wakad', 'Wanowrie', 'Wanwadi', 'encoded_project_name']
        ss=['Area', 'BHK', 'Bathroom', 'Best_school_count', 'Best_Restaurant_count', 'Best_ATM_count', 'Best_Hospital_count', 'ATM_count', 'Shopping_mall_count', 'School_count', 'Hospital_count', 'Restaurant_count', 'Exterior_ Asian Paint', 'Exterior_ Texture Paint', 'Exterior_ Apex Paint', 'Exterior_ Acrylic Emulsion Paint', 'Exterior_ Gypsum Finish', 'Exterior_ Apex Weatherproof Emulsion Paint', 'Exterior_ Emulsion Paint', 'Exterior_ Good Quality Paint', 'Exterior_ Weather Proof Paint', 'Exterior_ Water Resistant Paint', 'Exterior_ High Quality Texture Paint', 'Exterior_ POP Finish', 'Exterior_ Plastic Emulsion Paint', 'Interior_ Acrylic Paint', 'Interior_ Plastic Paint', 'Interior_ Emulsion Paint', 'Interior_ Acrylic Emulsion Paint', 'Interior_ Plastic Emulsion Paint', 'Interior_ Texture Paint', 'Interior_ POP Finish', 'Interior_ Paint, Distemper', 'Interior_ Sand Faced Plaster', 'Interior_ Cement Based Paint', 'Interior_ Semi Acrylic Paint', 'Interior_ Good Quality Paint', 'Interior_ Standard Paint', 'Interior_ Acrylic Emulsion Paint on POP Punning', 'Windows_ Aluminium Powder Coated Windows', 'Windows_ 3 Track UPVC Windows with SS Mosquito Net', 'Windows_ Aluminium Sliding Windows', 'Windows_ Anodized Aluminium Sliding', 'Windows_ Aluminium / UPVC / HardWood', 'Windows_ Powder coated aluminium sliding windows', 'Windows_ Aluminium Frames with Glazed Shutters', 'Windows_ Powder Coated Aluminum / UPVC Frames', 'Windows_ 2 Track UPVC Sliding Window with Mosquito Mesh Shutter', 'Windows_ Anodised / Powder Coated Aluminium Sliding Windows', 'Windows_ Standard', 'Windows_ M.S. Frame and Flush Door Shutter', 'Windows_ UPVC / Aluminium Windows', 'Windows_ Standard Windows', 'Windows_ Aluminum Sliding Window with Mosquito Mesh Shutters', 'Windows_ French Windows', 'Doors_ Veneered Door', 'Doors_ Moulded Designer Door', 'Doors_ Designer Door', 'Doors_ Decorative Flush Door', 'Doors_ Wooden Frame', 'Doors_ Elegant Door', 'Doors_ Pre Engineered Steel Frame with Wooden Shutters', 'Doors_ Aluminium with Wooden Shade', 'Doors_ Wood Frame', 'Doors_ Heavy Duty Wooden Laminated Doors', 'Doors_ Standard', 'Doors_ Decorative Flush with Hardwood Door Frames', 'Doors_ Beach Wood Frame', 'Doors_ Teak Wood Frame and Shutter', 'Electrical_ Concealed copper wiring', 'Electrical_ Concealed Copper Wiring with MCB/ ELCB', 'Electrical_ Copper Wiring in PVC Concealed Conduit', 'Electrical_ Concealed Copper Wiring', 'Electrical_ Havells/Anchor Make', 'Electrical_ Standard', 'Electrical_ Branded Concealed Copper Wiring with MCB / ELCB', 'Balcony_ Anti Skid Tiles', 'Balcony_ Vitrified Tiles', 'Balcony_ Anti Skid Vitrified Tiles', 'Balcony_ Marble Granite Tiles', 'Balcony_ Italian Marble', 'Toilets_ Anti Skid Tiles', 'Toilets_ CP Fittings of Jaquar / Marc or Equivalent', 'Toilets_ Branded CP Fittings & Sanitary Ware, Anti-Skid Tiles', 'Toilets_ Branded CP Fittings and Sanitary Ware', 'Toilets_ Ceramic Tiles Dado', 'Toilets_ Vitrified Tiles', 'Toilets_ Provision For Exhaust Fan', 'Toilets_ Anti Skid Tiles Dado', 'Toilets_ Sanitary fittings', 'Toilets_ Vitrified / Ceramic Tiles Dado', 'Toilets_ Branded CP Fitting', 'Toilets_ Kohler/Roca/American Standard or Equivalent Make', 'Toilets_ Ceramic Tiles Dado up to Lintel Level', 'Toilets_ Anti Skid Vitrified Tiles', 'Toilets_ Designer Tiles Dado up to 7 Feet Height Above Platform', 'Toilets_ Sanitary Ware / Parryware / Hindware or Equivalent Sanitary Fittings', 'Toilets_ Matt Finish Tiles', 'Toilets_ Marble Granite Tiles', 'Toilets_ Full Height Designer Tiles', 'Toilets_ ISI Branded Chromium Plated Tap', 'Toilets_ Parryware or Equivalent Sanitary Fittings', 'Toilets_ Provision for Geyser', 'Toilets_ Concealed Plumbing with Hot & Cold Mixer', 'Toilets_ Glazed Tiles', 'Toilets_ Vitrified Tiles (Kajaria)', 'Toilets_ High Quality CP Fittings', 'Toilets_ Italian Marble', 'Toilets_ Acid Resistant Tiles', 'Toilets_ EWC', 'Toilets_ Glazed Tiles Dado Up to Door Height', 'Toilets_ Granite Counter', 'Toilets_ Marble Flooring', 'Toilets_ Imported Marble Dado', 'Toilets_ Imported Marble', 'Toilets_ Mirror', 'Kitchen_ Granite platform with stainless steel sink', 'Kitchen_ Ceramic Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ - Granite counter in kitchen area', 'Kitchen_ Anti Skid Tiles Dado', 'Kitchen_ Modular Kitchen', 'Kitchen_ Stainless Steel Sink', 'Kitchen_ Ceramic Tiles Dado', 'Kitchen_ Italian Marble', 'Kitchen_ Branded CP fittings', 'Kitchen_ Vetrified tile flooring', 'Kitchen_ Designer Tiles Dado up to 2 Feet Height Above Platform', 'Kitchen_ Vitrified tiles on floor', 'Kitchen_ Ceramic Tiles', 'Kitchen_ Double bowl stainless steel sink', 'Kitchen_ Ceramic / Glazed Tiles Dado', 'Kitchen_ Concealed Plumbing with Premium Quality CP Fitting', 'Kitchen_ Dado Designer Wall Tiles', 'Kitchen_ Black Granite Platform', 'Kitchen_ Polished Granite Platform with Stainless Steel Sink', 'Kitchen_ Provision for Water Purifier', 'Kitchen_ 12 x 12 ceramic tiles', 'Kitchen_ Moduler Kitchen with Chimney & HOB', 'Kitchen_ Marble Granite Tiles', 'Kitchen_ C. P. Fittings.', 'Kitchen_ Granite Platform with Stainless Steel Sink and Drain Board', 'Kitchen_ Vitrified tile flooring in all rooms', 'Kitchen_ Vitrified tile flooring', 'Kitchen_ Italian Modular Cabinets', 'Kitchen_ RO System', 'Kitchen_ Floor Vitrified tile', 'Kitchen_ Designer glazed tile upto full height', 'Kitchen_ Green Marble', 'Kitchen_ Dishwasher', 'Kitchen_ Provision For Chimney And Water Purifier', 'Kitchen_ - Green marble/granite', 'Kitchen_ Modular Kitchen with Stainless Steel Sink', 'Kitchen_ Granite Flooring', 'Kitchen_ Ceramic Tiles Dado Till 600 mm above the Counter', 'Kitchen_ Elegant Vitrified Tiles', 'Kitchen_ Granite Platform', 'Kitchen_ Ceramic Tiles Dado above Working Platform', 'Kitchen_ Full marble flooring', 'Kitchen_ Anti Skid Vitrified Tiles', 'Other_Bedroom_ Vitrified Flooring', 'Other_Bedroom_ Marble Flooring', 'Other_Bedroom_ Vitrified tiles', 'Other_Bedroom_ 1mx1m vitrified tiles in bedrooms', 'Other_Bedroom_ Wooden Flooring', 'Other_Bedroom_ Vitrified floor tiles', 'Other_Bedroom_ Laminated Wooden', 'Other_Bedroom_ Granamite Tiles', 'Other_Bedroom_ Vitrified Flooring In Other Bedrooms', 'Other_Bedroom_ Floors Vitrified tiles flooring', 'Other_Bedroom_ Hardwood Flooring', 'Other_Bedroom_ All Bedrooms Imported engineered wooden flooring', 'Other_Bedroom_ Italian Marble', 'Other_Bedroom_ 800 x 800 vitrified ceramic tiles flooring', 'Other_Bedroom_ All bedrooms with wooden floorings', 'Other_Bedroom_ Marble Granite Tiles', 'Other_Bedroom_ Marble flooring in all bedrooms', 'Master_Bedroom_ Vitrified Flooring', 'Master_Bedroom_ - Master bedroom wooden flooring / other bedrooms vitrified tiles', 'Master_Bedroom_ Marble Flooring', 'Master_Bedroom_ Laminated Wooden Flooring', 'Master_Bedroom_ Wooden flooring', 'Master_Bedroom_ Best Quality Vitrified Tiles', 'Master_Bedroom_ Vitrified Tiled Flooring', 'Master_Bedroom_ - Wooden flooring in master bedroom', 'Master_Bedroom_ Laminated Wooden', 'Master_Bedroom_ 2 x 2 wooden finish vitrified tiles in Master bedroom', 'Master_Bedroom_ Granamite Tiles', 'Master_Bedroom_ Flooring Vitrified tiles', 'Master_Bedroom_ Master Bedrooms Wooden Flooring', 'Master_Bedroom_ Hardwood Flooring', 'Master_Bedroom_ Italian Marble', 'Master_Bedroom_ Engineered Wooden Flooring', 'Master_Bedroom_ Wooden finish vitrified tiles in master bedroom', 'Master_Bedroom_ 2 x 2 vitrified tiles drawing room , dining room, all bed rooms, kitchen and other area, wooden flooring in master bedroom', 'Master_Bedroom_ Marble Granite Tiles', 'Living_Dining_ Anti Skid Tiles', 'Living_Dining_ Marble Flooring', 'Living_Dining_ Morbonite Tiles', 'Living_Dining_ Anti Skid Vitrified Tiles', 'Living_Dining_ Marble Granite Tiles', 'Living_Dining_ Imported Marble', 'Living_Dining_ Granamite Tiles', 'Living_Dining_ Elegant Vitrified Tiles', 'Living_Dining_ Kota Stone', 'Living_Dining_ Ceramic Tiles', 'Living_Dining_ Italian marble', 'Living_Dining_ Acid Resistant Tiles', 'Building_Entrance Lobby', 'Building_Video Door Security', 'Building_Gazebo', 'Building_Open Parking', 'Building_Community Buildings', 'Building_Badminton Court', 'Building_Electrification(Transformer, Solar Energy etc)', 'Building_Fire Protection And Fire Safety Requirements', 'Building_Open Car Parking', 'Building_Multipurpose Hall', 'Building_Solar Lighting', 'Building_Intercom', 'Building_Multipurpose Room', 'Building_Solar Water Heating', 'Building_Waiting Lounge', 'Building_Infinity Pool', 'Building_Hospital', 'Building_Visitor Parking', "Building_Kid's Pool", 'Building_Banquet Hall', 'Building_Water Storage', 'Building_Jacuzzi', 'Building_Reflexology Park', 'Building_Staff Quarter', 'Building_Vaastu Compliant', 'Building_Spa/Sauna/Steam', 'Building_Squash Court', 'Building_Garbage Disposal', 'Building_Paved Compound', 'Building_Card Room', 'Building_Water Softner Plant', 'Building_Sun Deck', 'Building_Reading Lounge', 'Building_Laundromat', 'Building_Cricket Pitch', 'Building_RO Water System', 'Building_Valet Parking', 'Building_Service Lift', 'Building_Garden', 'Building_Fire Retardant Structure', 'Building_Lawn Tennis Court', 'Building_Pet Grooming', 'Building_Changing Room', 'Building_Salon', 'Building_Mini Theatre', 'Building_Golf Course', 'Building_Bar/Chill-out Lounge', 'Building_Aerobics Room', 'Building_Terrace Garden', 'Building_Open Air Theatre', 'Building_Flower Garden', 'Building_Spa', 'Building_Fountains', 'Building_Business Center', 'Building_Steam Room', 'Building_Restaurants/ Cafeterias', 'Building_Multi - Level Parking', 'Building_Billiards/Snooker Table', 'Building_Letter Box', 'Building_High Speed Elevators', 'Building_Semi Open Car Parking', 'Building_Theme Park', 'Building_Football Field', 'Building_Medical Facilities', 'Building_Medical Store/Pharmacy', 'Building_Doctor on call', 'Building_Foosball', 'Building_Smoke Detectors', 'Building_Reception/Waiting Room', 'Building_Concierge Service', 'Building_High-tech alarm system', 'Building_Manicured Garden', 'Building_DG Availability', 'Building_Beach Volley Ball Court', 'Building_Fire Alarm', 'Building_Water Supply', 'Building_Gas Pipeline', 'Building_Bore and Municipal Water', 'Building_Food Court', 'Building_Boom Barriers', 'Building_Helipad', 'Building_Board Games', 'Building_Automated Car Wash', 'Building_Anti-termite Treatment', 'Building_Sun Bathing', 'Building_Nature Club', 'Building_Cineplex', 'Building_Full Power Backup', 'Building_Advanced Security', 'Building_Sub-Station', 'Building_Club Rooftop', 'Anand Nagar', 'Aundh', 'BT Kawade Road', 'Balewadi', 'Baner', 'Bavdhan', 'Bibwewadi', 'Central Mumbai Suburbs', 'Chandan Nagar', 'Gahunje', 'Ghorpadi', 'Koregaon Park', 'Kothrud', 'Magarpatta City', 'Mahalunge', 'Pashan', 'Pashan Road', 'Paud Road', 'Pimple Nilakh', 'Shaniwar Peth', 'Sinhagad Road', 'Viman Nagar', 'Wadgaon Sheri', 'Wanowrie', 'Wanwadi']
        test2= pd.DataFrame([lp],columns= ss,dtype=float)
        y = regressor.predict(test2)
        print(y)
        range_val=f"{round(float(y)*.90)} - {round(float(y)*1.25)}"
        print("Outputtttt",range_val)
        return jsonify({"status":"Success","Message":range_val})


class getData(Resource):
    def get(self):
        return "Hello AVM USer"
    def post(self):
        data=json.loads(request.data)
        print(data)
        _instance = dataValidator(response=data)
        response=_instance.isTrue()

        if len(response)>0:
            _={
                "status":"error",
                "message":response
            },403
            return _
        else:
            final = _instance.predict(data)
            return final
            # return "ALL GOOOOOOOOOOOOOOD"
api.add_resource(getData,"/avm")

if __name__ == '__main__':
    app.run(debug=True,port=4000)
