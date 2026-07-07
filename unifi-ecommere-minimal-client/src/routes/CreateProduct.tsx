import React, { useCallback, useState, useEffect } from "react";
import { 
    Stack, Chip, Box, TextField, InputAdornment, 
    FormControl, InputLabel, MenuItem, Select,
    IconButton, TextareaAutosize, Alert, Snackbar, type AlertColor,
    FormHelperText, Button
} from "@mui/material"
import ShuffleIcon from '@mui/icons-material/Shuffle';
import NumberField from "../utils/NumberField";
import { lightTheme } from "@uiw/react-json-view/light";
import JsonView from "@uiw/react-json-view";
import JsonEditor, { type JsonValue } from "../utils/JsonEditor";
import { http } from "../API/axiosHTTP";
import { getAccessToken } from "../context/AuthContext";

const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

interface UnauthorizedUserResponse {
    error: string
}

interface ResponseToInvalidDatasheet {
    error: string
    datasheet: string
}

interface ResponseToInvalidStock {
    error: string
    stock: any
}

interface ResponseToInvalidCurrency {
    error: string,
    currency: string
}

interface ResponseToInvalidPrice {
    error: string,
    unit_price: string
}


const mockResponseToInvalidStock: ResponseToInvalidStock = {
    error: '...',
    stock: '...'
}

const mockResponseToInvalidDatasheet: ResponseToInvalidDatasheet = {
    error: '...',
    datasheet: '...'
}

const UnauthorizedUserResponseExample: UnauthorizedUserResponse = {
    error: '...'
}

const mockResponseToInvalidCurrency: ResponseToInvalidCurrency = {
    error: '...',
    currency: '...'
}

const mockResponseToInvalidPrice: ResponseToInvalidPrice = {
    error: '...',
    unit_price: '...'
}

export function generateBarcode(): string {
    const length = 127;
    if (!Number.isInteger(length) || length <= 0) {
        throw new RangeError(`length must be a positive integer, got ${length}`);
    }
    const maxValid = 256 - (256 % CHARS.length);
    const out: string[] = [];
    while (out.length < length) {
        const bytes = crypto.getRandomValues(new Uint8Array(length - out.length));
        for (const b of bytes) {
        if (b < maxValid) out.push(CHARS.charAt(b % CHARS.length));
        if (out.length === length) break;
        }
    }
    return out.join("");
}

interface CreateProductRequest {
    barcode: string;
    name: string;
    description: string;
    price: number;
    currency: string;
    stock: number;
    datasheet?: JsonValue | null;
    category: string;
}

const mockProductCreationRequest: CreateProductRequest = {
    barcode: "...",
    name: "...",
    description: "...",
    price: 0,
    currency: "...",
    stock: 0,
    datasheet: {
        key1: "...",
        key2: "..."
    },
    category: "..."
}

interface ProductCreationData {
    barcode: string
    name: string
    description: string | undefined
    price: number
    currency: string
    stock: number
    datasheet: JsonValue;
    category: string;
}
    
interface Category {
    name: string
}

const CreateProduct: React.FC = () => {
    const [isToastVisible, setIsToastVisible] = useState<boolean>(false)
    const [toastMessage, setToastMessage] = useState<string>('')
    const [toastState, setToastState] = useState<AlertColor>("info")
    
    const [rawDatasheet, setRawDatasheet] = useState<JsonValue>({})
    const [formData, setFormData] = useState<ProductCreationData>({
        barcode: '',
        name: '',
        description: '',
        price: 0,
        currency: '',
        stock: 0,
        datasheet: {},
        category: ''
    });

    const [categories, setCategories] = useState<Category[]>([]);

    const handleChange = (field: string) => (
        event: React.ChangeEvent<HTMLInputElement> | React.ChangeEvent<HTMLTextAreaElement>
    ) => {
        setFormData((prev: ProductCreationData) => ({ ...prev, [field]: event.target.value }));
    };

    const fetchCategoriesData = useCallback(async () => {
        await http.get('/staff/products/categories/')
            .then((response) => {
                setCategories(response.data.categories);
            })
            .catch((error) => {
                console.error('Error fetching categories data:', error);
                setToastMessage(`Error fetching categories data: ${error.data.detail || error.data.message || error.data.error}, status ${error.status}`);
                setToastState("error");
                setIsToastVisible(true);
            });
    }, [])

    useEffect(() => {
        fetchCategoriesData();
    }, []);


    const onSubmit = async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
    
        await http.post('/staff/products/create/', formData, {
            headers: {
                Authorization: `Bearer ${getAccessToken()}`,
            }
        })
        .then(
            (response) => {
                    setToastMessage(`Product created successfully: ${response.data.product} in ${response.data.category}`);
                    setToastState("success");
                    setIsToastVisible(true);
            }
        )
        .catch(
            error => {
                setToastMessage(`Error creating product: ${error.response?.data?.detail || error.response?.data?.message || error.response?.data?.error}, status ${error.status}`);
                setToastState("error");
                setIsToastVisible(true);
            }
        )
    }

    return (
        <main>
            <Stack direction="column" sx={{
                alignItems: "flex-start"
            }}>
                <h1>Create A Product</h1>
                <Chip label="POST" color="post" variant="outlined" />
            </Stack>

            <section>
                <h2>Introduction</h2>
                <p>Use this endpoint to create a new product for the specified category.</p>
            </section>

            <section>
                <h2>Request format</h2>
                <JsonView value={mockProductCreationRequest} style={lightTheme} />
            </section>

            <section>
                <h2>Exceptions</h2>
                <ul>
                    <li>
                        <h3>Incomplete response</h3>
                        <p>The client request is missing required fields, the server responds with a <code>400</code> status and an error message formatted as follows.</p>
                        <JsonView value={UnauthorizedUserResponseExample} style={lightTheme} />
                    </li>
                    <li>
                        <h3>User doesn't have permissions to add Product or Product Variant</h3>
                        <p>When the request comes from a user without the required role(s) to create a product, the server responds with a <code>401</code> status and an error message.</p>
                        <JsonView value={UnauthorizedUserResponseExample} style={lightTheme} />
                    </li>
                    <li>
                        <h3>Bad parameters</h3>
                        <ul>
                            <li>
                                <h4>
                                    <pre><code>Datasheet</code></pre> is not a valid JSON object.
                                </h4>
                                <p>Datasheet must be a valid JSON object encoded as a string. In case you fail to comply to this contract, you will receive a <code>400</code> response with the following interface.</p>
                                <JsonView value={mockResponseToInvalidDatasheet} style={lightTheme} />
                            </li>

                            <li>   
                                <h4>
                                    <pre><code>Stock</code></pre> must be an integer.
                                </h4>
                                <p>Stock must be a non-negative integer. Any value that's not integer, including floating point with decimal figures, will cause you to receive a <code>400</code> response with the following interface.</p>
                                <JsonView value={mockResponseToInvalidStock} style={lightTheme} />
                            </li>

                            <li>
                                <h4>
                                    <pre><code>Currency</code></pre> must be a valid ISO 4217 currency code.
                                </h4>
                                <p>To avoid potential ambiguity about how a currency must be specified, the server expects a standardized code for the currency. Expecting an uppercase, 3 characters long code representing the currency. In case of failure, a <code>400</code> status response with the following interface will be returned.</p>
                                <JsonView value={mockResponseToInvalidCurrency} style={lightTheme} />
                            </li>

                            <li>
                                <h4>
                                    <pre><code>price</code></pre> must be a non-negative, real number.
                                </h4>
                                <p>The price of the product must be non-negative. In case this expectation is not met you will receive a <code>400</code> response with this interface:</p>
                                <JsonView value={mockResponseToInvalidPrice} style={lightTheme} />
                            </li>
                            
                            <li>
                                <h4>Duplication</h4>
                                <p>If a product with the same barcode already exist creation will fail with a responde status <code>409</code> and the response will have the following interface:</p>
                                <JsonView value={UnauthorizedUserResponseExample} style={lightTheme} />
                            </li>
                        </ul>
                    </li>
                </ul>
            </section>

            <section>
                <h2>Create a Product</h2>
                <Box component="form" onSubmit={onSubmit} noValidate sx={{marginTop: 2, marginBottom: 2}}>
                    <Stack spacing={2}>
                        <TextField
                            label="Barcode"
                            value={formData.barcode}
                            slotProps={{
                                input: {
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <IconButton
                                            edge="start"
                                            onClick={() => {
                                                setFormData((prev: ProductCreationData) => ({ ...prev, barcode: generateBarcode() }));
                                            }}
                                        >
                                            <ShuffleIcon />
                                        </IconButton>
                                    </InputAdornment>
                                ),
                                }
                            }}
                            fullWidth
                        />

                        <TextField
                            label="name"
                            value={formData.name}
                            onChange={handleChange('name')}
                            fullWidth
                        />

                        <TextareaAutosize
                            minRows={3}
                            placeholder="Description"
                            style={{ width: '100%' }}
                            value={formData.description}
                            onChange={handleChange('description')}
                            />

                        <NumberField
                            label="Unit Price"
                            min={-Number.MAX_VALUE}
                            max={Number.MAX_VALUE}
                            defaultValue={0}
                            value={formData.price}
                            onValueChange={
                                (event) => {
                                    setFormData((prev: ProductCreationData) => ({ ...prev, price: Number(event) }));
                                }
                            }
                            size="small"
                            />

                        <FormControl fullWidth>
                        <InputLabel id="unit-price-currency">Currency</InputLabel>
                            <Select
                                labelId="unit-price-currency"
                                id="unit-price-currency-select"
                                value={formData.currency}
                                label="Age"
                                onChange={(changeEvent) => {
                                    setFormData(
                                        (prev: ProductCreationData) => ({ ...prev, currency: changeEvent.target.value })
                                    )
                                }}
                            >
                                <MenuItem value={'EUR'}>EUR</MenuItem>
                            </Select>
                        </FormControl>

                        <NumberField
                            label="Stock"
                            min={0}
                            max={Number.MAX_VALUE}
                            defaultValue={0}
                            value={formData.stock}
                            onValueChange={
                                (event) => {
                                    setFormData((prev: ProductCreationData) => ({ ...prev, stock: Number(event) }));
                                }
                            }
                            size="small"
                        />

                        <JsonEditor
                            value={rawDatasheet}
                              onChange={(newValue) => {
                                setRawDatasheet(newValue);
                                setFormData(prev => ({
                                    ...prev,
                                    datasheet: newValue,
                                }));
                            }}
                        />
                        <FormHelperText>
                            Datasheet
                        </FormHelperText>

                        <FormControl fullWidth>
                        <InputLabel id="product-category">Category</InputLabel>
                            <Select
                                labelId="product-category"
                                id="product-category-select"
                                value={formData.category}
                                label="Category"
                                onChange={(changeEvent) => {
                                    setFormData(
                                        (prev: ProductCreationData) => ({ ...prev, category: changeEvent.target.value })
                                    )
                                }}
                                sx={{
                                    marginBottom: 4
                                }}
                            >
                                {
                                    categories.map(
                                        category => {
                                            return (
                                                <MenuItem value={category.name} key={category.name}>{category.name}</MenuItem>
                                            )
                                        }
                                    )
                                }
                            </Select>
                        </FormControl>
                                                
                        <Snackbar
                            open={isToastVisible}
                            autoHideDuration={6000}
                            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                            onClose={() => setIsToastVisible(false)}
                        >
                            <Alert severity={toastState} variant="filled" sx={{ width: "100%" }}>
                                { toastMessage }
                            </Alert>
                        </Snackbar>

                        <Button type="submit" variant="contained" size="large" fullWidth>
                            Create Product
                        </Button>
                    </Stack>
                </Box>
            </section>
        </main>
    )
}

export default CreateProduct