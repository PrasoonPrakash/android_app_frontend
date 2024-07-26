import 'package:aanchal_ai/global_vars.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:io';
import 'dart:convert';
import 'package:csv/csv.dart';

class ResultsPage extends StatefulWidget {
  const ResultsPage({super.key});

  @override
  State<ResultsPage> createState() => _ResultsPageState();
}

class _ResultsPageState extends State<ResultsPage> {
  String text = " ";
  //String translation = " ";
  bool fp=false;
  List<List<dynamic>> _data=[];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(100),
        child: AppBar(
          toolbarHeight: 100,
          title: Text(
            "Prediction",
            style: TextStyle(
                fontWeight: FontWeight.w600, fontSize: 22, color: Colors.black),
          ),
          leading: IconButton(
            icon: Icon(Icons.arrow_back_ios),
            onPressed: () {
              //Navigator.pop(context);
              Navigator.of(context).popUntil((route) => route.isFirst);
            },
          ),
          centerTitle: true,
          elevation: 6,
          shadowColor: Colors.black,
          backgroundColor: Colors.white,
          surfaceTintColor: Colors.white,
          //automaticallyImplyLeading: false,
        ),
      ),
      body: Center(
          child: SingleChildScrollView(
            padding:EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              answer != null?answer!:"Prediction will be shown here",
              style: TextStyle(
                    fontWeight: FontWeight.w600,
                    fontSize: 25,
                    color: Colors.black)
            ),
            SizedBox(height: 20,),
            ElevatedButton(
                onPressed: () async {
                  final response = await http
                      .get(Uri.parse('http://10.222.76.205:6000/hindi'));
                  final decoded =
                      json.decode(response.body) as Map<String, dynamic>;
                  setState(() {
                    text = decoded["transcript"];
                  });
                  final path = "/sdcard/Download/transcriptions/";
                  final dictToSave = Directory(path);
                  if (!await dictToSave.exists()) {
                    await dictToSave.create(recursive: true);
                  }
                  var fileName = "${name}_hindi.txt";
                  String filePath = path + fileName;
                  final File file = File(filePath);
                  await file.writeAsString(text);
                },
                style: ElevatedButton.styleFrom(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(5),
                    ),
                    backgroundColor: const Color.fromARGB(255, 177, 214, 225),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 32, vertical: 16)),
                child: Text("HINDI TEXT",
                    style: TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 15,
                        color: Colors.black))),
            SizedBox(
              height: 15,
            ),
            ElevatedButton(
              onPressed: () async {
                final response = await http
                    .get(Uri.parse('http://10.222.76.205:6000/english'));
                final decoded =
                    json.decode(response.body) as Map<String, dynamic>;
                setState(() {
                  text = decoded["translation"];
                });
                final path = "/sdcard/Download/translations/";
                final dictToSave = Directory(path);
                if (!await dictToSave.exists()) {
                  await dictToSave.create(recursive: true);
                }
                var fileName = "${name}_english.txt";
                String filePath = path + fileName;
                final File file = File(filePath);
                
                await file.writeAsString(text);
              },
              style: ElevatedButton.styleFrom(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(5),
                    side:
                        BorderSide(color: Color.fromARGB(255, 177, 214, 225))),
                backgroundColor: const Color.fromARGB(255, 232, 243, 246),
                padding:
                    const EdgeInsets.symmetric(horizontal: 35, vertical: 16),
              ),
              child: Text("ENGLISH TEXT",
                  style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 15,
                      color: Colors.black)),
            ),
            SizedBox(
              height: 15,
            ),
            ElevatedButton(
              onPressed: () async {
                setState(() {
                  fp=true;
                });
                final response = await http
                    .get(Uri.parse('http://10.222.76.205:6000/data'));
                final decoded =
                    json.decode(response.body) as Map<String, dynamic>;
                setState(() {
                  text = decoded.toString();
                });
                print(text);
                // final path = "/sdcard/Download/data/";
                // final dictToSave = Directory(path);
                // if (!await dictToSave.exists()) {
                //   await dictToSave.create(recursive: true);
                // }
                // List<List<dynamic>> _listData= const CsvToListConverter().convert(text);
                // setState(() {
                //   _data=_listData;
                // });
                // var fileName = "${name}_data.csv";
                // String filePath = path + fileName;
                // final File file = File(filePath);
                // await file.writeAsString(text);
              },
              style: ElevatedButton.styleFrom(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(5),),
                backgroundColor: const Color.fromARGB(255, 177, 214, 225),
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              ),
              child: Text("EXTRACTED FEATURES",
                  style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 15,
                      color: Colors.black)),
            ),
            SizedBox(height: 20,),
            
            Text(text,
                style: TextStyle(
                    fontWeight: FontWeight.w400,
                    fontSize: 15,
                    color: Colors.black)),
            // SizedBox(
            //   height: 100,
            //   child: ListView.builder(
            //     itemCount: _data.length,
            //     itemBuilder: (_,index){
            //       return Card(
            //         margin: const EdgeInsets.all(3),
            //         color: index==0 ? Colors.redAccent: Colors.white,
            //         child: ListTile(
            //           leading: Text(_data[index][0].toString()),
            //           title: Text(_data[index][1]),
            //         ),
            //       );
            //     },
            //     scrollDirection: Axis.horizontal,

            //   ),
            //   //fp=false;
            // ),
          ],
        ),
      )),
    );
  }
}
