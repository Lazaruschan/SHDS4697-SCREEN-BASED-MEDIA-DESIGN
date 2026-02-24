# me - this DAT
# scriptOp - the OP which is cooking
#
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.

# Initialize variables
counter = 0
S1 = 0
S2 = 0
S3 = 0
S4 = 0
S5 = 0
S6 = 0
pause_until = 0  # Time when pause ends

def onSetupParameters(scriptOp):
	page = scriptOp.appendCustomPage('Custom')
	p = page.appendFloat('Valuea', label='Value A')
	p = page.appendFloat('Valueb', label='Value B')
	p = page.appendPulse('Reset', label='Reset All Values')
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	if par.name == 'Reset':
		resetAllValues()
	return

def resetAllValues():
	global counter, S1, S2, S3, S4, S5, S6, pause_until
	counter = 0
	S1 = 0
	S2 = 0
	S3 = 0
	S4 = 0
	S5 = 0
	S6 = 0
	pause_until = 0
	print("All values have been reset")
	return

def findLargestValue():
	values = [S1, S2, S3, S4, S5, S6]
	max_val = max(values)
	max_index = values.index(max_val) + 1  # +1 to get S1-S6 numbering
	return max_index, max_val

def onCook(scriptOp):
	global counter, S1, S2, S3, S4, S5, S6, pause_until
	
	scriptOp.clear()
	
	# Check if we're in a pause state
	current_time = op('constant1').time.seconds
	if current_time < pause_until:
		remaining = int(pause_until - current_time)
		print(f"Paused: {remaining} seconds remaining")
		scriptOp.appendRow(['Status', f'PAUSED ({remaining}s left)'])
		scriptOp.appendRow(['Variable', 'Value'])
		scriptOp.appendRow(['Counter', counter])
		scriptOp.appendRow(['S1', S1])
		scriptOp.appendRow(['S2', S2])
		scriptOp.appendRow(['S3', S3])
		scriptOp.appendRow(['S4', S4])
		scriptOp.appendRow(['S5', S5])
		scriptOp.appendRow(['S6', S6])
		return
	
	counter += 1
	print("Counter: ", counter)
	
	# Check if counter exceeded 20000
	if counter > 500:
		counter = 0
		print("Counter reset to 0")
		
		# Find which S value is largest
		largest_s, largest_val = findLargestValue()
		print(f"S{largest_s} has the largest value: {largest_val}")
		
		# Pause for 1 minute
		pause_until = current_time + 60  # 60 seconds = 1 minute
		print(f"Pausing for 1 minute until: {pause_until}")
	
	# Check for OSC input
	oscin = op('chopto1')
	oscValue = oscin[0, 0]  # Get the first value from OSCIN1
	
	# Increment the appropriate variable based on OSC value
	if oscValue == 0:
		S1 += 1
		print("S1 incremented to:", S1)
	elif oscValue == 1:
		S2 += 1
		print("S2 incremented to:", S2)
	elif oscValue == 2:
		S3 += 1
		print("S3 incremented to:", S3)
	elif oscValue == 3:
		S4 += 1
		print("S4 incremented to:", S4)
	elif oscValue == 4:
		S5 += 1
		print("S5 incremented to:", S5)
	elif oscValue == 5:
		S6 += 1
		print("S6 incremented to:", S6)
	
	# Output current values to the DAT
	scriptOp.appendRow(['Status', 'RUNNING'])
	scriptOp.appendRow(['Variable', 'Value'])
	scriptOp.appendRow(['Counter', counter])
	scriptOp.appendRow(['S1', S1])
	scriptOp.appendRow(['S2', S2])
	scriptOp.appendRow(['S3', S3])
	scriptOp.appendRow(['S4', S4])
	scriptOp.appendRow(['S5', S5])
	scriptOp.appendRow(['S6', S6])
	
	return