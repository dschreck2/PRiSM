//
//  TextLog.swift
//  frontend
//
//  Created by David Schreck on 5/14/21.
//

import Foundation

struct TextLog: TextOutputStream {
    static var shared = TextLog()
    
    private init() {}
    
    /// Appends the given string to the stream.
    mutating func write(_ string: String) {
        
        
        let logPath = Bundle.main.resourcePath! + "/frontend_log.txt"
        let logURL = URL(fileURLWithPath: logPath)
        
        do {
            let handle = try FileHandle(forWritingTo: logURL)
            handle.seekToEndOfFile()
            handle.write(string.data(using: .utf8)!)
            handle.write("\n".data(using: .utf8)!)
            handle.closeFile()
        } catch {
            print(error.localizedDescription)
            do {
                try string.data(using: .utf8)?.write(to: logURL)
            } catch {
                print(error.localizedDescription)
            }
        }
    }
}
