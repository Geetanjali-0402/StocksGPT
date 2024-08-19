// stockPriceChart.tsx
import React, { useEffect } from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout } from 'plotly.js';

interface Props {
  plotData?: {
    data: Data[];
    layout: Partial<Layout>;
  };
}


const StockPriceChart: React.FC<Props> = ({ plotData }) => {
  useEffect(() => {
    // console.log("New plotData received in StockPriceChart:", plotData);
  }, [plotData, plotData?.data]);

  if (!plotData || !plotData.data) {
    return <div>Loading chart or data not available...</div>;
  }
  const config = {
    responsive: true,
  };

  // console.log("Rendering with data:", plotData.data);

  // return <div>{plotData ? "Data loaded" : "Loading data..."}</div>;

  return <Plot 
  data={plotData.data} 
  layout={{...plotData.layout, autosize:true}} 
  config={config}
  // style={{ width: "100%", height: "100%" }}
  // useResizeHandler={true}
  /> 
};

export default React.memo(StockPriceChart);
