import pysubdisc
import pandas
import matplotlib.pyplot as plt


# Load the Adult data
data = pandas.read_csv('adult.txt')

# Examine input data
table = pysubdisc.loadDataFrame(data)
print(table.describeColumns())



print('\n\n******* Section 1 *******\n')

# SECTION 1
# Set up SD with default settings, based on a 'single nominal' setting

''' a single binary target, a target value 'gr50K' '''
sd = pysubdisc.singleNominalTarget(data, 'target', 'gr50K')

# Print the default settings
print(sd.describeSearchParameters())

# Do the actual run
sd.run()

# Print the subgroups
print(sd.asDataFrame())


print('\n\n******* Section 2 *******\n')

# SECTION 2
sd = pysubdisc.singleNominalTarget(data, 'target', 'gr50K')
sd.qualityMeasure = 'CORTANA_QUALITY'
sd.qualityMeasureMinimum = 0.1

'''Set the numeric strategy from 'bins' to ''best'.'''
sd.numericStrategy = 'NUMERIC_BEST'

sd.run(verbose=False)

print(sd.asDataFrame())


print('\n\n******* Section 3 *******\n')

# SECTION 3
sd = pysubdisc.singleNominalTarget(data, 'target', 'gr50K')
sd.qualityMeasure = 'CORTANA_QUALITY'

'''Set measure minimum to 0.25'''
sd.qualityMeasureMinimum = 0.25

'''setting the refinement depth to 2'''
sd.searchDepth = 2

sd.numericStrategy = 'NUMERIC_BEST'

sd.run(verbose=False)

print(sd.asDataFrame())



print('\n\n******* Section 4 *******\n')

# SECTION 4

'''same as Section 3'''
sd_no_filter = pysubdisc.singleNominalTarget(data, 'target', 'gr50K')
sd_no_filter.qualityMeasure = 'CORTANA_QUALITY'
sd_no_filter.qualityMeasureMinimum = 0.25
sd_no_filter.searchDepth = 2

''' switching Filter Subgroups checkbox off'''
sd_no_filter.filterSubgroups = False
sd_no_filter.numericStrategy = 'NUMERIC_BEST'

sd_no_filter.run(verbose=False)

print(sd_no_filter.asDataFrame())
print("Subgroup count with filtering turned ON: ", len(sd.asDataFrame()))	# reusing the result from Section 3 here
print("Subgroup count with filtering turned OFF: ", len(sd_no_filter.asDataFrame()))

# Compute pattern team of size 3 from the found subgroups

'''Compute a Pattern Team of size 3.'''
size = 3
patternTeam, grouping  = sd_no_filter.getPatternTeam(size, returnGrouping=True)
print(patternTeam)

''' Inspect the contents'''

df = sd_no_filter.asDataFrame()
for i in range(size):
    print(df[grouping[i]])


print('\n\n******* Section 5 *******\n')

# SECTION 5
sd = pysubdisc.singleNominalTarget(data, 'target', 'gr50K')

'''Set the measure minimum to 0.0'''
sd.qualityMeasureMinimum = 0.0

sd.numericStrategy = 'NUMERIC_BEST'

'''Leave refinement depth at 2 for the remainder'''
sd.searchDepth = 2

'''Relative Lift quality measure'''
sd.qualityMeasure = 'RELATIVE_LIFT'

sd.run(verbose=False)

print(sd.asDataFrame())



print('\n\n******* Section 6 *******\n')

# SECTION 6

''' set the minimum coverage to 5'''
sd.minimumCoverage = 5

''' the minimum quality to 3'''
sd.qualityMeasureMinimum = 3
sd.run(verbose=False)

print(sd.asDataFrame())



print('\n\n******* Section 7 *******\n')

# SECTION 7

'''Select 'single numeric' as target type, and 'age' as the target attribute'''
sd = pysubdisc.singleNumericTarget(data, 'age')

'''Leave refinement depth at 2 for the remainder'''
sd.searchDepth = 2
sd.numericStrategy = 'NUMERIC_BEST'

'''Set measure minimum to 0.0'''
sd.qualityMeasureMinimum = 0

'''Set the minimum coverage back to 10%'''
# sd.minimumCoverage = 10

sd.run(verbose=False)

'''the average age'''
print("Average age in the data: ", data['age'].mean())
print(sd.asDataFrame())

'''the age distribution of the best subgroup compared to that of the entire dataset'''
model = sd.getModel(0, relative=True)
model.plot()
plt.savefig('age_distribution.pdf')



print('\n\n******* Section 8 *******\n')

# SECTION 8
# run 100 swap-randomised SD runs in order to determine the minimum required quality to reach a significance level alpha = 0.05
sd.computeThreshold(setAsMinimum=True, verbose=False)

sd.run(verbose=False)

print("Minimum quality for significance: ", sd.qualityMeasureMinimum)
print(sd.asDataFrame())


print('\n\n******* Section 9 *******\n')

# SECTION 9

# Load the Ames Housing data
data = pandas.read_csv('ameshousing.txt')

# Examine input data
table = pysubdisc.loadDataFrame(data)
print(table.describeColumns())

'''select 'Lot Area' and 'SalePrice'as the primary and secondary target.'''
sd = pysubdisc.doubleRegressionTarget(data, 'Lot Area', 'SalePrice')

sd.run(verbose=False)

# Print first subgroup
print(sd.asDataFrame().loc[0])


