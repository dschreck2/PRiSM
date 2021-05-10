//
//  ContentView.swift
//  frontend
//
//  Created by David Schreck on 4/13/21.
//

import SwiftUI
import PythonKit

extension View {
    @ViewBuilder func hidden(_ shouldHide: Bool) -> some View {
        switch shouldHide {
        case true: self.hidden()
        case false: self
        }
    }
}

struct ContentView: View {
    @State var showStopButton: Bool = false
    @State var startStopButtonText: String = "Start"
    @State var isCollecting: Bool
    @State var osVersion: String
    @State var processes: [Database.Process]
    @State var cpuCurrent: Double
    @State var cpuAverage: Double
    @State var cpuCores: Int
    @State var ramCurrent: Double
    @State var ramTotal: Double
    @State var ramAverage: Double
    @State var diskUsed: Double
    @State var diskTotal: Double
    
    let db = Database()
    
    
    var metricCollector: PythonObject
    
    var body: some View {
        VStack(alignment: .leading) {
            HStack(alignment: .center) {
                Button(action: {
                    self.runPythonCode()
                    showStopButton.toggle()
                    if showStopButton {
                        startStopButtonText = "Stop"
                    } else {
                        startStopButtonText = "Start"
                    }
                }) {
                    Text(self.startStopButtonText)
                }.disabled(self.isCollecting && !showStopButton)
                
                Button(action: {
                    print("Generating report")
                }) {
                    Text("Generate Report")
                }
                

                Text("Host OS Version: \(self.osVersion)").hidden(self.osVersion.count == 0)
                
                
            }
            .padding([.top, .leading, .bottom])
            
            HStack(spacing: 400) {
                VStack(alignment: .leading) {
                    Text("CPU Usage")
                    Text(String(format: "%.2f%% Current", self.cpuCurrent))
                    Text(String(format: "%.2f%% Average", self.cpuAverage))
                    Text("\(self.cpuCores) Cores")
                }
                
                VStack(alignment: .leading) {
                    Text("RAM Usage")
                    Text(String(format: "%.2fG Current", self.ramCurrent))
                    Text(String(format: "%.2fG Total", self.ramTotal))
                    Text(String(format: "%.2fG Average", self.ramAverage))
                }
                
                VStack(alignment: .leading) {
                    Text("Disk Usage")
                    Text(String(format: "%.2f%% Used", self.diskUsed / self.diskTotal * 100)).hidden(self.diskTotal == 0)
                    Text(String(format: "%.2fG Used", self.diskUsed))
                    Text(String(format: "%.2fG Total", self.diskTotal))
                }
            }.padding(.leading, 10)
            
            
            
            HStack() {
                Text("COMMAND").frame(width: 175, alignment: .topLeading)
                Text("PID").frame(width: 100, alignment: .topLeading)
                Text("PPID").frame(width: 100, alignment: .topLeading)
                Text("% MEM").frame(width: 100, alignment: .topLeading)
                Text("% CPU").frame(width: 100, alignment: .topLeading)
                Text("USER").frame(width: 225, alignment: .topLeading)
//                Text("START TIME").frame(width: 150, alignment: .topLeading)
                Text("WALLTIME").frame(width: 100, alignment: .topLeading)
                Text("CPUTIME").frame(width: 100, alignment: .topLeading)
                Text("THREADS").frame(width: 100, alignment: .topLeading)
            }
            .padding(.leading, 10)
            .padding(.top, 20)
            
            List(self.processes) { process in
                Text("\(process.name)").frame(width: 175, alignment: .topLeading)
                Text("\(process.pid)").frame(width: 100, alignment: .topLeading)
                Text("\(process.ppid)").frame(width: 100, alignment: .topLeading)
                Text(String(format: "%.2f", process.memoryUsage)).frame(width: 100, alignment: .topLeading)
                Text(String(format: "%.2f", process.cpuUsage)).frame(width: 100, alignment: .topLeading)
                Text("\(process.username)").frame(width: 225, alignment: .topLeading)
//                Text("\(process.dateTime)").frame(width: 150, alignment: .topLeading)
                Text("\(process.walltime)").frame(width: 100, alignment: .topLeading)
                Text("\(process.cputime)").frame(width: 100, alignment: .topLeading)
                Text("\(process.threads)").frame(width: 100, alignment: .topLeading)
                
            }
//            List {
//                VStack(alignment: .leading) {
//                    ForEach(self.processes) { process in
//                        HStack() {
//                            Text("\(process.name)").frame(width: 100, alignment: .topLeading).border(Color.red)
////                            Text(String(format: "%-25@ %-10d %-10d", process.name, process.pid, process.ppid))
//                            Text("\(process.pid)").frame(width: 100, alignment: .topLeading).border(Color.blue)
//                            Text("\(process.ppid)").frame(width: 100, alignment: .topLeading).border(Color.green)
//
////                            Text("\(process.ppid)")
//                        }
//                    }
//                }
//            }
        }
    }
    
    func startMetricCollection() {
        let queue = DispatchQueue(label: "prism.queue")
        var exitTimer = false
        queue.async {
            print("Start metric collection")
            self.isCollecting = true
            self.metricCollector.main()
            self.isCollecting = false
            exitTimer = true
            print("Finished metric collection")
        }
        
        // query database every 15 seconds
        var runCount = 0
        
        var connectionIsOpen = false
        
        func queryDatabase() {
            // connect to database
            if !connectionIsOpen {
                connectionIsOpen = db.openConnection()
            }

            if connectionIsOpen {
                // query latest host info
                let host = db.getHost()

                // query all processes
                if host != nil {
                    self.osVersion = host!.osVersion
                    print("get processes")
                    self.processes = db.getProcesses(hostId: host!.id)

                    print("get cpu usage")
                    self.cpuCurrent = db.getCurrentCpuUsage(hostId: host!.id)
                    self.cpuAverage = db.getAverageCpuUsage(hostId: host!.id)
                    self.cpuCores = host!.numCores

                    print("get ram usage")
                    self.ramCurrent = db.getCurrentRamUsage(hostId: host!.id)
                    self.ramTotal = host!.totalRam
                    self.ramAverage = db.getAverageRamUsage(hostId: host!.id)

                    print("get disk usage")
                    self.diskUsed =  db.getCurrentDiskUsage(hostId: host!.id)
                    self.diskTotal = host!.totalDisk
                } else {
                    print("Skipping process query since host id is nil")
                }
            } else {
                print("Skipping database queries since there is no connection to the database")
            }
        }
        
        print("test")
        
        Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { timer in
            if connectionIsOpen {
                timer.invalidate()
                return
            }

            queryDatabase()
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 10.0) {
            // Put your code which should be executed with a delay here
            NSLog("start collection loop")
            Timer.scheduledTimer(withTimeInterval: 15.0, repeats: true) { timer in
                NSLog("Timer beginning")
                if exitTimer {
                    timer.invalidate()
                    print("Timer exit")
                    return
                }

                queryDatabase()

                print("Timer fired: \(runCount)")
                runCount += 1
            }
        }

//        Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { timer in
//            if connectionIsOpen {
//                timer.invalidate()
//                return
//            }
//
//            queryDatabase()
//        }
////
//        Timer.scheduledTimer(withTimeInterval: 15.0, repeats: true) { timer in
//            print("Timer beginning")
//            if exitTimer {
//                timer.invalidate()
//                print("Timer exit")
//                return
//            }
//
//            queryDatabase()
//
//            print("Timer fired: \(runCount)")
//            runCount += 1
//        }
        print("test2 ")
    }
    
    func stopMetricCollection() {
        let fileManager = FileManager.default
        let runFile = Bundle.main.resourcePath! + "/run.txt"
        do {
            // Check if file exists
            if fileManager.fileExists(atPath: runFile) {
                // Delete file
                try fileManager.removeItem(atPath: runFile)
            } else {
                print("Skipping file removal, run file does not exist")
            }
        }
        catch let error as NSError {
            print("Unable to delete run file: \(error)")
        }
    }
    
    func runPythonCode() {
        if ( self.isCollecting ) {
            self.stopMetricCollection()
        } else {
            self.stopMetricCollection()
            self.startMetricCollection()
        }
    }
    
    init() {
        let sys = Python.import("sys")
        let resourcesPath = Bundle.main.path(forResource: "backend", ofType: nil )!
        sys.path.append(resourcesPath.description)
        
        self.metricCollector = Python.import("main")
        self.isCollecting = false
        self.osVersion = ""
        self.processes = []
        
        self.cpuCurrent = 0
        self.cpuAverage = 0
        self.cpuCores = 0
        self.ramCurrent = 0
        self.ramTotal = 0
        self.ramAverage = 0
        self.diskUsed = 0
        self.diskTotal = 0
    }
}



struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .padding()
            
    }
}
