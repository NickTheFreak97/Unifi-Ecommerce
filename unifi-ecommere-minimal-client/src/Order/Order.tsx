import React, { useState } from 'react'
import { Stepper, Step, StepLabel, Box } from '@mui/material'
import OrderDetail from './OrderDetail';
import PaymentDetails from './PaymentDetails';



const Order: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => setActiveStep((s) => s + 1);

  const steps: { label: string; render: () => React.ReactNode }[] = [
    {
      label: 'Order Details',
      render: () => <OrderDetail onSubmit={handleNext} />,
    },
    {
      label: 'Payment',
      render: () => { return <PaymentDetails />},
    },
  ];


  return (
    <Box>
      <Stepper activeStep={activeStep}>
        {steps.map(({ label }) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Box sx={{ mt: 3 }}>
        {steps[activeStep].render()}
      </Box>
    </Box>
  );
}

export default Order