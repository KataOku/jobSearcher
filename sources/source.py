import json

class Adv_source():

    def __init__(self, name, website, roles=["software tester","software developer", "QA"], date=None):
        self.source_name=name
        self.source_website=website
        self.last_checked_date=date
        if type(roles)==list:
            self.positions=roles
        else: self.positions=[roles]
        self.prev_advs=self.__get_prev_advs()


    def __get_prev_advs(self):
        """Checks for previously saved advertisements, returns dictionary with results"""
        try:
            advs_file=open(f"adverts/{self.source_name.lower()}.json", "r")
            loaded_file=json.load(advs_file)
            return loaded_file['prev_advs']
        except: 
            return {}

    def __remove_closed_advs(self, adverts):
        """Checks for closed advertisements and removes them"""
        to_remove=[]
        for adv in self.prev_advs.keys():
            if adv not in adverts.keys():
                to_remove.append(adv)        
        for adv in to_remove:
            self.prev_advs.pop(adv)



    def check_for_new(self):
        """Checks for new advertisements, prints the result and saves it in file"""
        adverts=self.get_results()
        self.__remove_closed_advs(adverts)
        new_advs={}
        for adv in adverts.keys():
            if adv not in self.prev_advs.keys(): 
                new_advs[adv]=adverts[adv]
        if new_advs:
            print("\n\nNew advertisements from "+self.source_name+":\n\n")
            for adv in new_advs.keys():
                print(new_advs[adv]['title']+"\n"+new_advs[adv]['href']+"\n")
        else:
            print("\n\nThere are no new advertisements from "+self.source_name+".\n\n")
        self.save_advertisements(new_advs)


    def save_advertisements(self, new_advs):
        """Saves advertisements in .json file"""
        with open(f"adverts/{self.source_name.lower()}.json", "w") as advs_file:
            self.prev_advs.update(new_advs)
            json.dump(vars(self), advs_file, indent=4)        
        return True


    

