//
//  Database.swift
//  frontend
//
//  Created by David Schreck on 5/4/21.
//

import Foundation
import GRDB

class Database {
//    var dbQueue: DatabaseQueue!
    var dbPool: DatabasePool!
    
    
    func openConnection() -> Bool {
        let resourcesPath = Bundle.main.path(forResource: "db", ofType: nil )!
        let dbPath = "\(resourcesPath.description)/prism.db"
        
        do {
            var config = Configuration()
            config.readonly = true
            config.maximumReaderCount = 10
            
            self.dbPool = try DatabasePool(path: dbPath, configuration: config)
            TextLog.shared.write("Established database connection")
            return true
        } catch {
            TextLog.shared.write("Unable to establish database connection \(error)")
            return false
        }
    }
    
    func getHost() -> Host? {
        var host: Host?
        do {
            try self.dbPool.read { db in
                host = try Host.fetchOne(db, sql: "SELECT * from host WHERE id=(SELECT max(id) FROM host)")!
            }
        } catch {
            TextLog.shared.write("Unable to get host: \(error)")
        }
        
        return host
    }
    
    func getProcesses(hostId: Int) -> [Process] {
        var processes: [Process] = []
        
        do {
            try self.dbPool.read { db in
                processes = try Process.fetchAll(db, sql: "SELECT * from process WHERE hostId==\(hostId) AND COUNT==(SELECT MAX(count) from process WHERE hostId==\(hostId)) ORDER BY cpuUsage DESC LIMIT 20")
            }
        } catch {
            TextLog.shared.write("Unable to get processes: \(error)")
        }
        
        return processes
    }
    
    func getCurrentCpuUsage(hostId: Int) -> Double {
        var cpuUsage: Double = 0
        
        do {
            try self.dbPool.read { db in
                cpuUsage = try Double.fetchOne(db, sql: "SELECT used from cpu WHERE id=(SELECT max(id) FROM cpu WHERE hostId==\(hostId))")!
            }
        } catch {
            print("Unable to get current cpu usage: \(error)")
        }
        
        return cpuUsage
    }
    
    func getAverageCpuUsage(hostId: Int) -> Double {
        var cpuAverage: Double = 0
        
        do {
            try self.dbPool.read { db in
                cpuAverage = try Double.fetchOne(db, sql: "SELECT AVG(used) from cpu WHERE hostId==\(hostId)")!
            }
        } catch {
            print("Unable to get average cpu usage: \(error)")
        }
        
        return cpuAverage
    }
    
    func getCurrentRamUsage(hostId: Int) -> Double {
        var ramUsage: Double = 0
        
        do {
            try self.dbPool.read { db in
                ramUsage = try Double.fetchOne(db, sql: "SELECT used from ram WHERE id=(SELECT max(id) FROM ram WHERE hostId==\(hostId))")!
            }
        } catch {
            print("Unable to get current ram usage: \(error)")
        }
        
        return ramUsage
    }
    
    func getAverageRamUsage(hostId: Int) -> Double {
        var ramAverage: Double = 0
        
        do {
            try self.dbPool.read { db in
                ramAverage = try Double.fetchOne(db, sql: "SELECT AVG(used) from ram WHERE hostId==\(hostId)")!
            }
        } catch {
            print("Unable to get average ram usage: \(error)")
        }
        
        return ramAverage
    }
    
    func getCurrentDiskUsage(hostId: Int) -> Double {
        var diskUsage: Double = 0
        
        do {
            try self.dbPool.read { db in
                diskUsage = try Double.fetchOne(db, sql: "SELECT used from disk WHERE id=(SELECT max(id) FROM disk WHERE hostId==\(hostId))")!
            }
        } catch {
            print("Unable to get current disk usage: \(error)")
        }
        
        return diskUsage
    }
    
    func helloWorld() {
        print("hello there")
    }
    
    
    
    struct Host: Identifiable, FetchableRecord {
        init(row: Row) {
            id = row["id"]
            dateTime = row["dateTime"]
            numCores = row["numCores"]
            osVersion = row["osVersion"]
            totalDisk = row["totalDisk"]
            totalRam = row["totalRam"]
        }
        
        var id: Int
        var dateTime: String
        var numCores: Int
        var osVersion: String
        var totalDisk: Double
        var totalRam: Double
    }
    
    struct Disk: Identifiable, FetchableRecord {
        init(row: Row) {
            id = row["id"]
            hostId = row["hostID"]
            count = row["count"]
            dateTime = row["dateTime"]
            used = row["used"]
        }
        
        var id: Int
        var hostId: Int
        var count: Int
        var dateTime: String
        var used: Double
    }
    
    struct Ram: Identifiable, FetchableRecord {
        init(row: Row) {
            id = row["id"]
            hostId = row["hostID"]
            count = row["count"]
            dateTime = row["dateTime"]
            used = row["used"]
        }
        
        var id: Int
        var hostId: Int
        var count: Int
        var dateTime: String
        var used: Double
    }
    
    struct Cpu: Identifiable, FetchableRecord {
        init(row: Row) {
            id = row["id"]
            hostId = row["hostID"]
            count = row["count"]
            dateTime = row["dateTime"]
            used = row["used"]
        }
        
        var id: Int
        var hostId: Int
        var count: Int
        var dateTime: String
        var used: Double
    }
    
    struct Process: Identifiable, FetchableRecord {
        init(row: Row) {
            id = row["id"]
            hostId = row["hostID"]
            count = row["count"]
            dateTime = row["dateTime"]
            name = row["name"]
            pid = row["pid"]
            ppid = row["ppid"]
            memoryUsage = row["memoryUsage"]
            cpuUsage = row["cpuUsage"]
            username = row["username"]
            threads = row["threads"]
            walltime = row["walltime"]
            cputime = row["cputime"]
        }
        
        var id: Int
        var hostId: Int
        var count: Int
        var dateTime: String
        var name: String
        var pid: Int
        var ppid: Int
        var memoryUsage: Double
        var cpuUsage: Double
        var username: String
        var threads: Int
        var walltime: String
        var cputime: String
    }
}
