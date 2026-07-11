import React from 'react'
import { useState } from 'react';
import { Stepper, Step, StepLabel, Button, Box, Stack, TextField } from '@mui/material'
import OrderDetail from './OrderDetail';

interface StepPageProps {
  onNext?: () => void;
  onBack?: () => void;
}

function ProfileForm({ onNext, onBack }: StepPageProps) {
  return (
    <Box>
      {/* Form content */}
      <Stack spacing={2} sx={{ mb: 4 }}>
        <TextField label="First Name" />
        <TextField label="Last Name" />
      </Stack>

      {/* Navigation */}
      <Stack direction="row" spacing={2}>
        <Button onClick={onBack}>Back</Button>
        <Button variant="contained" onClick={onNext}>Next</Button>
      </Stack>
    </Box>
  );
}


function ReviewPage({ onBack }: StepPageProps) {
  return <div>Review <Button onClick={onBack}>Back</Button></div>;
}

const steps: { label: string; render: () => React.ReactNode }[] = [
  {
    label: 'Order Details',
    render: () => <OrderDetail onSubmit={() => {}} />,
  },
  {
    label: 'Payment',
    render: () => { return <div>Lorem ipsum</div>},
  },
];


const Order: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => setActiveStep((s) => s + 1);
  const handleBack = () => setActiveStep((s) => s - 1);

  const ActiveComponent = steps[activeStep].render;

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

export default Order;