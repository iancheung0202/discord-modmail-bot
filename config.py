### ------ STAFF POSITION ------ ###
def getHighestRole(ppl):
  roles = ppl.roles
  roles.reverse()
  highestRole = str(roles[0])

  if "Owner" in highestRole: # If staff has role containing "owner"
    highestRole = "Server Owner" # Make his/her title "Server Owner"
  elif "Co-owner" in highestRole:
    highestRole = "Server Co-owner"
  elif "Admin" in highestRole:
    highestRole = "Discord Admin"
  elif "Moderator" in highestRole:
    highestRole = "Discord Mod"
    
  # IF YOU THINK THIS IS UNNECESSARY, COMMENT OUT LINE 18 AND UNCOMMENT LINE 17 AND CHANGE THE TITLE TO WHATEVER YOU LIKE
  # return "Server Staff Team"
  return highestRole

PREFIX = "!"
DESCRIPTION = ""
LOG_CHANNEL = 944840833440567306
GUILD_ID = 943302660025634836
CATEGORY_ID = 944841033177497600
TIMEOUT = 5
STATUS = "DM me for help"
TOKEN = "NzMyODk3ODA3NTU1NjI1MDQx.Xw7SRQ.wgSJTcidm4_aRvxuc9HJ0iv5En4"

# PLEASE ALSO TYPE THIS TO YOUR TERMINAL: pip install discord-components

hi = "Hey there! \n\nThank you for reaching out to our community team. How may we help you today? Please describe the matter as detailed as possible so we could assist you further! However, if we do not receive any reply from you, your thread will be disregarded and closed shortly.\n\nAll the best"
transferred = "Hey there,\n\nWe have notified the respective persons regarding this thread. They will be getting back to you as soon as they can! Meanwhile, if you additional information, hit us up!\n\nAll the best"
reported = "Hey there,\n\nThank you for bringing this to our attention. We have started an investigation and needed action will be taken soon. We will be getting back to you shortly.\n\nMeanwhile, if you have anymore additional information, simply reply back and we'll also look into it!\n\nAll the best"
morehelp = "Is there anything else we can help you with today? If not, we will be closing this thread shortly within 24 hours!"
noreply = "Hey there,\n\nThis is a gentle reminder that this thread will be closed shortly if you do not reply to it within a 24-hour time frame! Thank you for your attention!\n\nCheers"
canthelp = "Hey there\n\nWe regret to inform you that we are unable to assist you regarding to the topic you mentioned. If you need anymore help, just reply back and we'll also look into the issue!\n\nAll the best"