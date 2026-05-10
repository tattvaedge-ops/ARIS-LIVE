// C:\AGENTIC AI- ARIS\aris-mobile\services\api.ts

const API_BASE_URL =
  'https://aris-live-production.up.railway.app';

async function handleResponse(
  response: Response
) {
  const data = await response.json();

  if (
    !response.ok ||
    data.success === false
  ) {
    throw new Error(
      data.message ||
        data.reply ||
        'Request failed'
    );
  }

  return data;
}

// ==========================================
// LOGIN
// ==========================================
export async function loginUser(
  email: string,
  password: string
) {
  const response = await fetch(
    `${API_BASE_URL}/api/login`,
    {
      method: 'POST',
      headers: {
        'Content-Type':
          'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  return handleResponse(response);
}

// ==========================================
// SIGNUP
// ==========================================
export async function signupUser(
  email: string,
  password: string
) {
  const response = await fetch(
    `${API_BASE_URL}/api/signup`,
    {
      method: 'POST',
      headers: {
        'Content-Type':
          'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  return handleResponse(response);
}

// ==========================================
// CHAT
// ==========================================
export async function sendMessage(
  message: string,
  authToken: string
) {
  const response = await fetch(
    `${API_BASE_URL}/chat`,
    {
      method: 'POST',
      headers: {
        'Content-Type':
          'application/json',
        Cookie: `aris_token=${authToken}`,
      },
      body: JSON.stringify({
        message,
      }),
    }
  );

  return handleResponse(response);
}

// ==========================================
// BUY TOKENS
// ==========================================
export async function buyTokens(
  authToken: string
) {
  const response = await fetch(
    `${API_BASE_URL}/buy_tokens`,
    {
      method: 'GET',
      headers: {
        Cookie: `aris_token=${authToken}`,
      },
    }
  );

  return handleResponse(response);
}

// ==========================================
// IMAGE UPLOAD + ANALYSIS
// ==========================================
export async function uploadImage(
  imageUri: string,
  authToken: string
) {
  const formData = new FormData();

  formData.append(
    'image',
    {
      uri: imageUri,
      name: 'question.jpg',
      type: 'image/jpeg',
    } as any
  );

  const response = await fetch(
    `${API_BASE_URL}/api/upload-image`,
    {
      method: 'POST',
      headers: {
        Cookie: `aris_token=${authToken}`,
      },
      body: formData,
    }
  );

  return handleResponse(response);
}