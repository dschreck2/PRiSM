//
//  ContentView.swift
//  frontend
//
//  Created by David Schreck on 4/13/21.
//

import SwiftUI
import PythonKit

struct ContentView: View {
//    var dirPath = "/Users/schreck3/Library/Developer/Xcode/DerivedData/frontend-bbshmjpaceggeldbhmplgvkavwlp/Build/Products/Debug/frontend.app/Contents/Resources/backend"
    
    var pyBuildPath: String {
        var s  = "/"
        s += Bundle.main.infoDictionary?["TargetName"] as! String // add TargetName == $(TARGET_NAME) in info.plist
        s += ".app/Contents/Resources/backend" // relative path within my swift project containing py scripts
        return s
    }
    
    var body: some View {
        VStack(alignment: .leading) {
            HStack(alignment: .center) {
                Button(action: {
                    self.runPythonCode()
                }) {
                    Text("Start")
                }
            }
            .padding([.top, .leading, .bottom])
            Rectangle()
        }
    }
    
    func runPythonCode() {
        let sys = Python.import("sys")
        
        if let resourcesPath = Bundle.main.path(forResource: "backend", ofType: nil ) {
            sys.path.append(resourcesPath.description)
            
            let example = Python.import("main")
            let response = example.setPath(resourcesPath)
            print(response)
        } else {
            print("bad log info here or something")
        }
    }
    
    
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
