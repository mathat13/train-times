import requests
import re

def websiteFetcher(orient, fro, to = '', add = ''):
    '''Returns html from the national rail website based on the url specified using the requests package.'''
    url1 = 'http://ojp.nationalrail.co.uk/service/ldbboard/{}/{}/{}/{}'.format(orient, fro, to, add) # Allows 'user input' for the url.
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}# Disguises the website request.
    payload = {'name':'Chrome'}
    r = requests.get(url1, headers = headers)
    r = r.text
    r = re.sub(r'\t', '', r)# Removes \t from html.
    r = re.sub(r'\n', '', r)#Removes \n from html.
    r = re.sub(r'&nbsp;', ' ', r)#Certain parts of had this string between useful string information, needed to be removed. 
    return r


#--------------------------------------------

def trainTimeFinder(html):
    '''Takes the html and breaks it down into useful information, then prints this information.'''
    data = re.findall(r'<td.*?>\s*(.*?)\s*</td>', html, re.DOTALL)# Finds all relevent information(Train time, delays, station, platform).   

    i = 0
    while i < len(data)-1:
        
        if len(data[i+2]) >= 10: # if train is late, other options are 'Delayed', 'On time' or ' Cancelled'
            data[i+2] = data[i+2][:5] #Change time to first 5 characters of this entry, this is the time that the train will arrive
        data[i+4] = re.findall(r'\"(.*?)\"', data[i+4])[0] #Strips the url from rest of html in this index position, can affix it to end of base url to get further info on train.
        if i == 0:
            print('\n')# Formatting.
        print('Train {}'.format(int(i/5)))# Round about way of printing natural numbers.
        print('Train time: {0}\t\t Expected time: {2}\nDestination: {1}\t Platform: {3}\n'.format(data[i], data[i+1], data[i+2], data[i+3])) # Print all the information
        i += 5 # Move onto the next train info pack
    return 0

#---------------------------------------------
def stationHelper(station):
    with open('station_codes.txt', 'r') as txtfile: #Opens the txt file of all stations and station codes in the UK.
        codes = txtfile.read()
        if station in codes:
            finder = re.findall(station + '\s[A-Z]{3}', codes)# Checks if there are multiple occurences of station specified.
            
            if len(finder) != 1:                                              #If there are 2 or more stations.
                stn_decide = re.findall(station + r'\s?(.+)\s[A-Z]{3}', codes)# Finds additional words after choice of station but not station code.

                while True: #Loop to get station code
                    i = 0
                    resolver = ''
                    
                    while i < len(stn_decide): # creates message for choice of multiple stations.
                        resolver += stn_decide[i]
                        if i < len(stn_decide)-1: # inbetween station text
                            resolver += ' or '
                        if i == len(stn_decide)-1: # Message for end of string
                            resolver += ' (please enter words as shown): ' #Helpful message.
                        i += 1
                        
                    inpt_rslvr = input(resolver)# Choice of station.
                    if inpt_rslvr in stn_decide:# If valid choice,
                        station += ' ' + inpt_rslvr # Add extra choice onto search pattern.
                        break
                
            stn = re.findall(station + r'\s([A-Z]{3})', codes)# Find station code for choice of station
            return stn[0] #Returns Correct station code.
        else:
            return 'Sort it out mate'# If you see this message, catastropic failure is likely.
#---------------------------------------------

def checker(arg1, arg2, arg3):
    '''Determines if choice, journ_type and start_station are of the correct type.'''
    if arg1 == 'l' or arg1 == 'j': # 'l' and 'j' are acceptable
        if arg2 == 'a' or arg2 == 'd': # 'a' and 'd' are acceptable
            if len(arg3) == 3: # input put through stationHelper, return value should be 3 letter station code
                return True # If all true, return true, else return error messages for user and false for python
            print('No such station, please retry.')
            return False
        print('The choices are "a" and "d".')
        return False
    print('Good try, next time attempt to type "l" or "j".')
    return False
#---------------------------------------------
def main():    
    while True:
        choice = input('Live times or journey planner? (l/j): ').lower()
        journ_type = input('Arrivals or departures? (a/d):  ').lower()
        start_station = stationHelper(input('Where from/ to:').lower())

        if checker(choice, journ_type, start_station): # Check all choices are valid.
            if choice == 'l':
                
                if journ_type == 'a':# Arrivals.
                    trainTimeFinder(websiteFetcher('arr', start_station))  #live boards, arrivals at station     
                elif journ_type == 'd':# Departures.
                    trainTimeFinder(websiteFetcher('dep', start_station))  #live boards, departures from station
                
            elif choice == 'j':
                toe = stationHelper(input('Where toe/ from: '))
                
                if journ_type == 'a':
                    trainTimeFinder(websiteFetcher('arr', start_station, to = toe, add = 'From'))    #live boards, arrivals from station to station      
                elif journ_type == 'd':
                    trainTimeFinder(websiteFetcher('dep', start_station, to = toe, add = 'To'))  #live boards, departures from station to station

        again = input('Again (y/n)? ').lower()# Repeater.
        if again == 'y':
            continue
        else:
            break

main()
