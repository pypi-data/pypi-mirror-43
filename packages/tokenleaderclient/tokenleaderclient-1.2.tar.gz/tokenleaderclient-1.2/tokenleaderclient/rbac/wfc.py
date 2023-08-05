class WorkFuncContext():
    username = ''
    org = ''
    orgunit = ''
    department = ''
    name = ''
    email = ''
    
    def setcontext(self, uname, em, wfc):
        self.username = uname
        self.email = em
        self.org = wfc.get('org')
        self.orgunit = wfc.get('orgunit')
        self.department = wfc.get('department')
        self.name = wfc.get('name')            
        
    
    
    