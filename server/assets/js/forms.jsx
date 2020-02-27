/* jshint esversion: 9 */

import React, { useReducer, useContext, useEffect, useState } from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';
import { subForms, initialFormState, actionTypes, inputs, reducer, FormDispatch, useStyles } from './form-constants';
import { FormFieldWrapper, SubmitField, SubmitButton, NextButton, SubFormTitle, CurrencyField } from './form-components';

export { SuperForm };


// Form component for holding overall form data
function SuperForm(props) {
    // Fetch defined styling
    const classes = useStyles(props);

    // Use reducer hook to handle form data
    const [state, dispatch] = useReducer(reducer, initialFormState);

    // Use effect hook for api validation
    // No need to reset validationInput to some default value, since this
    // effect will only run when it changes.
    useEffect(() => {
        // TODO: Make this do mad fetching to get validated values
        switch (state.validationInput) {
            case inputs.buying:
                // TODO: Validate buying party!

                // TODO: Make this condition actually API-related
                if (state.buyingParty.includes("test")) {
                    dispatch({
                        type: actionTypes.provideSuggestions,
                        input: inputs.buying,
                        suggestions: ["Sixty", "Nine", "Dudes!"]
                    });
                }

                break;

            case inputs.selling:
                // TODO: Validate selling party!

                // TODO: Make this condition actually API-related
                if (state.sellingParty.includes("test")) {
                    dispatch({
                        type: actionTypes.provideSuggestions,
                        input: inputs.selling,
                        suggestions: ["Whoa", "Excellent", "*Electric Guitar Noises*"]
                    });
                }

                break;

            case inputs.product:
                // TODO: Validate product!

                if (state.productName.includes("test")) {
                    dispatch({
                        type: actionTypes.provideSuggestions,
                        input: inputs.product,
                        suggestions: ["Strange things are", "afoot at", "the Circle-K"]
                    });
                }
                // // Dispatch validated values to form!
                // dispatch({
                //     input: inputs.buying,
                //     type: actionTypes.new,
                //     newValue: state[inputs.buying] + " (validated by product)"
                // });
                // dispatch({
                //     input: inputs.selling,
                //     type: actionTypes.new,
                //     newValue: state[inputs.selling] + " (validated by product)"
                // });
                // dispatch({
                //     input: inputs.product,
                //     type: actionTypes.new,
                //     newValue: state[inputs.product] + " (validated by product)"
                // });            

                break;

            // TODO: Below validations!

            case inputs.quantity:
                break;

            case inputs.uCurr:
                break;

            case inputs.uPrice:
                if (isNaN(state.underlyingPrice)) {
                    dispatch({
                        type: actionTypes.markIncorrect,
                        input: inputs.uPrice
                    });
                } else {
                    dispatch({
                        type: actionTypes.markCorrect,
                        input: inputs.uPrice
                    });
                }

                break;
            
            case inputs.mDate:
                break;
            
            case inputs.nCurr:
                break;
            
            case inputs.sPrice:
                break;

            default:
                break;
        }
    }, [state.validationInput]);  // Only perform effect when validationInput changes

    // Use effect hook for logging corrections!
    useEffect(() => {
        const [field, oldVal, newVal] = state.correctionFields.correctionLog.slice(-1);
        // TODO: Send fields to API!
    }, [state.correctionFields.correctionLog]);  // Only perform effect when correctionFields changes

    // Use effect hook for submitting form
    useEffect(() => {
        // TODO: Get this to actually do some submitting you muppet
        if (state.submitNow) {
            document.write("Submitted! (Obviously not this is debug text)");
        }
    }, [state.submitNow]);

    // Render the specific subform that's currently meant to be on screen
    let elem = null;
    switch (state.currentForm) {
        case subForms[1]:
            elem = (
                <Paper elevation={3} className={classes.formContainer}>
                    <FormDispatch.Provider value={dispatch}>
                        <SubFormOne fields={{...state}} />
                    </FormDispatch.Provider>
                </Paper>
            );
            break;

        case subForms[2]:
            elem = (
                <Paper elevation={3} className={classes.formContainer}>
                    <FormDispatch.Provider value={dispatch}>
                        <SubFormTwo fields={{...state}} />
                    </FormDispatch.Provider>
                </Paper>
            );
            break;

        case subForms[3]:
            // TODO: Implement sub form 3!
            elem = null;
            break;

        case subForms.submit:
            elem = (
                <Paper elevation={3} className={classes.formContainer}>
                    <FormDispatch.Provider value={dispatch}>
                        <SubmitForm fields={{...state}} />
                    </FormDispatch.Provider>
                </Paper>
            );
            break;
    }

    return elem;
}


// First subform component - only need 3, so can be custom
function SubFormOne(props) {
    // Fetch defined styling
    const classes = useStyles(props);

    // Only let them progress if all fields are non-empty and there are no
    // corrections left
    let anyEmptyOrError = (
        props.fields.correctionFields[inputs.buying].length > 0
        || props.fields.correctionFields[inputs.selling].length > 0
        || props.fields.correctionFields[inputs.product].length > 0
        || props.fields.sellingParty === ""
        || props.fields.buyingParty === ""
        || props.fields.productName === ""
    );

    // Render sub-form within a grid
    return (
    <Grid
        container
        justify="center"
        alignContent="center"
        className={classes.formContainer}
        direction="column"
        spacing={3}
    >
        <CssBaseline />
        <Grid item>
            <SubFormTitle>Step 1 of 4</SubFormTitle>
        </Grid>
        <Grid item className={classes.formItemContainer}>
            <FormFieldWrapper
                id={inputs.buying}
                label="Buying Party"
                value={props.fields.buyingParty}
                suggestions={props.fields.correctionFields[inputs.buying]}
                incorrectField={props.fields.incorrectFields[inputs.buying]}
                helperText="Please enter the buying party."
            />
        </Grid>
        <Grid item className={classes.formItemContainer}>
            <FormFieldWrapper
                id={inputs.selling}
                label="Selling Party"
                value={props.fields.sellingParty}
                suggestions={props.fields.correctionFields[inputs.selling]}
                incorrectField={props.fields.incorrectFields[inputs.selling]}
                helperText="Please enter the selling party."
            />
        </Grid>
        <Grid item className={classes.formItemContainer}>
            <FormFieldWrapper
                id={inputs.product}
                label="Product Name"
                value={props.fields.productName}
                suggestions={props.fields.correctionFields[inputs.product]}
                incorrectField={props.fields.incorrectFields[inputs.product]}
                helperText="Please enter the product name."
            />
        </Grid>
        <Grid item className={classes.formItemContainer}>
            {anyEmptyOrError ? <NextButton disabled /> : <NextButton />}
        </Grid>
    </Grid>
    );
}


function SubFormTwo(props) {
    // Fetch defined styling
    const classes = useStyles(props);

    // Only let them progress if all fields are non-empty and there are no
    // corrections left
    let anyEmptyOrError = (
        props.fields.correctionFields[inputs.uCurr].length > 0
        || props.fields.correctionFields[inputs.uPrice].length > 0
        || props.fields.underlyingCurrency === ""
        || props.fields.underlyingPrice === ""
    );

    // Render sub-form within a grid
    return (
        <Grid
            container
            justify="center"
            alignContent="center"
            className={classes.formContainer}
            direction="column"
            spacing={3}
        >
            <CssBaseline />
            <Grid item>
                <SubFormTitle>Step 2 of 4</SubFormTitle>
            </Grid>
            <Grid item className={classes.formItemContainer}>
                <CurrencyField
                    id={inputs.uCurr}
                    label="Underlying Currency"
                    value={props.fields.underlyingCurrency}
                    suggestions={props.fields.correctionFields[inputs.uCurr]}
                    currencies={props.fields.currencies}
                />
            </Grid>
            <Grid item className={classes.formItemContainer}>
                <FormFieldWrapper
                    id={inputs.uPrice}
                    label="Underlying Price"
                    value={props.fields.underlyingPrice}
                    suggestions={props.fields.correctionFields[inputs.uPrice]}
                    incorrectField={props.fields.incorrectFields[inputs.uPrice]}
                    helperText="Please enter the underlying currency and price."
                />
            </Grid>
            <Grid item className={classes.formItemContainer}>
                {anyEmptyOrError ? <NextButton disabled /> : <NextButton />}
            </Grid>
        </Grid>
        );
}


// Subform for the final Submit page, where the user checks everything
function SubmitForm(props) {
    // Fetch defined styling
    const classes = useStyles(props);

    // If any fields are blank, you can't submit!
    const fields = Object.values(inputs).map(input => props.fields[input]);
    let anyInputEmpty = fields.some(field => field === "");

    // Render sub-form within a grid
    return (
        <Grid
            container
            justify="center"
            alignContent="center"
            className={classes.formContainer}
            direction="column"
            spacing={0}
        >
            <Grid item>
                <SubFormTitle>Step 4 of 4: Final Check</SubFormTitle>
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.buying}
                    label="Buying Party"
                    value={props.fields.buyingParty}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.selling}
                    label="Selling Party"
                    value={props.fields.sellingParty}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.product}
                    label="Product Name"
                    value={props.fields.productName}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.quantity}
                    label="Product Quantity"
                    value={props.fields.quantity}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.uPrice}
                    label="Underlying Price"
                    value={props.fields.underlyingPrice}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.uCurr}
                    label="Underlying Currency"
                    value={props.fields.underlyingCurrency}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.mDate}
                    label="Maturity Date"
                    value={props.fields.maturityDate}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.nCurr}
                    label="Notional Currency"
                    value={props.fields.notionalCurrency}
                />
            </Grid>
            <Grid item className={classes.submitItemContainer}>
                <SubmitField
                    id={inputs.sPrice}
                    label="Strike Price"
                    value={props.fields.strikePrice}
                />
            </Grid>
            <Grid item className={classes.submitButton}>
            {anyInputEmpty ? <SubmitButton disabled/> : <SubmitButton/>}
            </Grid>
        </Grid>
    );
}
