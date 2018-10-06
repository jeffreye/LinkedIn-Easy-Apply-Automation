class JobData:
    def __init__(self, jobTitle, company, link, city):
        self.jobTitle = jobTitle
        self.company = company
        self.link = link
        self.city = city

    def __str__(self):
        return self.jobTitle+','+self.company+','+self.link+','+self.city

    def __unicode__(self):
        return self.jobTitle+','+self.company+','+self.link+','+self.city

    def __repr__(self):
        return str(self)
