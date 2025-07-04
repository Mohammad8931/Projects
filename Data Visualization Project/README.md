# Data Visualization Project

This data analysis project examines how major economic crises affected commodity prices over the past decades. Using historical commodity price data from 1980 to 2016, it analyzes the impact of the 2008 Financial Crisis, European Debt Crisis, and Oil Price Crash through comprehensive data visualization.

## Project Description

The analysis focuses on understanding market volatility during economic turmoil by examining commodity price patterns during three major economic events. The project creates interactive visualizations and statistical analysis to reveal how different asset classes respond to economic shocks and geopolitical events.

## Dataset Overview
- **Time Period**: 1980-2016 (monthly data)
- **Total Commodities**: 53 different commodities
- **Market Indexes**: 10 comprehensive price indexes
- **Data Size**: 450 rows × 64 columns (~388 KB)
- **Source**: International Monetary Fund (IMF)
- **Reference Year**: 2005 (index baseline)

## Economic Events Analyzed

### 1. 2008 Global Financial Crisis (2008-2012)
- Collapse of financial institutions and housing markets
- Severe recession with prolonged recovery periods
- Impact on global commodity markets and supply chains

### 2. European Debt Crisis (2009-2013)
- Sovereign debt crisis in Greece, Portugal, and Spain
- Required extensive bailouts and austerity measures
- Eurozone structural challenges and economic divergence

### 3. Oil Price Crash (2014-2016)
- Sharp decline in oil prices due to oversupply
- OPEC production decisions and geopolitical tensions
- Impact on oil-producing countries and related industries

## Technical Implementation

### Data Analysis Tools
- **Python Libraries**: Pandas, NumPy for data manipulation
- **Visualization**: Matplotlib, Seaborn, Plotly for interactive charts
- **Statistical Analysis**: Comprehensive correlation and trend analysis
- **Interactive Elements**: Dynamic charts with user controls

### Analysis Components
1. **Price Trend Analysis**: Long-term commodity price movements
2. **Volatility Assessment**: Market stability during crisis periods
3. **Correlation Studies**: Relationships between different commodities
4. **Crisis Impact Measurement**: Before/during/after comparisons
5. **Recovery Pattern Analysis**: Post-crisis market behavior

## Key Findings

### Market Behavior Patterns
- **Energy Commodities**: Most volatile during geopolitical events
- **Agricultural Products**: Stable but affected by economic uncertainty
- **Metals**: Strong correlation with industrial demand cycles
- **Precious Metals**: Flight-to-safety behavior during crises

### Crisis-Specific Insights
- **2008 Crisis**: Broad-based commodity decline with metals hit hardest
- **European Crisis**: Regional impact with energy sector volatility
- **Oil Crash**: Sector-specific with broader economic implications

## Visualization Features

### Interactive Dashboards
- **Time Series Plots**: Dynamic price evolution over time
- **Correlation Heatmaps**: Relationship analysis between commodities
- **Crisis Timeline Views**: Event-specific market impact visualization
- **Comparative Analysis**: Before/during/after crisis comparisons

### Statistical Visualizations
- **Distribution Analysis**: Price change patterns during crisis periods
- **Volatility Metrics**: Standard deviation and variance analysis
- **Recovery Curves**: Post-crisis price normalization patterns
- **Sector Comparison**: Different commodity categories performance

## Installation & Setup
```bash
pip install pandas numpy matplotlib seaborn plotly jupyter
```

## Usage
```bash
# Open the analysis notebook
jupyter notebook FinalProject-DataVisualization.ipynb

# Run cells sequentially to:
# 1. Load and clean data
# 2. Generate crisis timeline analysis
# 3. Create interactive visualizations
# 4. Export charts and insights
```

## File Structure
```
Data Visualization Project/
├── FinalProject-DataVisualization.ipynb  # Main analysis notebook
├── commodity-prices.csv                  # Historical price data
└── README.md                            # Project documentation
```

## Analysis Methodology

### Data Preprocessing
- **Missing Value Treatment**: Handling gaps in historical data
- **Index Normalization**: Standardizing to 2005 baseline year
- **Time Series Alignment**: Consistent monthly data points
- **Outlier Detection**: Identifying and handling extreme values

### Crisis Period Definition
```python
# Crisis periods for analysis
crisis_periods = {
    'Financial_Crisis': ('2008-01', '2012-12'),
    'European_Crisis': ('2009-01', '2013-12'),
    'Oil_Crash': ('2014-01', '2016-12')
}
```

### Visualization Approach
- **Multi-panel Layouts**: Comprehensive view of different metrics
- **Color-coded Analysis**: Crisis periods highlighted distinctly
- **Interactive Elements**: Zoom, filter, and selection capabilities
- **Export Quality**: High-resolution charts for reports

## Key Insights

### Market Resilience Factors
- **Diversification Benefits**: Different commodities show varying crisis sensitivity
- **Geographic Impact**: Regional crises have different global effects
- **Recovery Timeframes**: Commodities recover at different rates
- **Policy Effectiveness**: Government interventions show measurable impacts

### Investment Implications
- **Portfolio Strategy**: Crisis-aware commodity allocation
- **Risk Management**: Understanding volatility patterns
- **Timing Decisions**: Entry/exit points during market stress
- **Hedging Opportunities**: Using commodity relationships for protection

## Applications
- **Academic Research**: Economic crisis impact studies
- **Investment Strategy**: Portfolio management and risk assessment
- **Policy Analysis**: Understanding crisis transmission mechanisms
- **Market Education**: Teaching economic relationship concepts

## Technical Performance
- **Data Processing Speed**: Efficient handling of 36-year dataset
- **Visualization Quality**: Publication-ready chart generation
- **Interactive Performance**: Smooth real-time chart updates
- **Memory Efficiency**: Optimized for large-scale time series data

## Future Enhancements
- **Real-time Data Integration**: Live commodity price feeds
- **Machine Learning Models**: Predictive crisis impact analysis
- **Expanded Coverage**: Additional commodities and economic indicators
- **Web Dashboard**: Interactive online visualization platform 