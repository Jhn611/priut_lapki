import axios from "axios";
const BASE_URL = "http://26.48.41.80:8000";

export async function req(params, request, type, API_TOKEN) {
  try {
    const config = {
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${API_TOKEN}`,
        "Content-Type": "application/json",
      },
    };
    console.log(API_TOKEN)

    let response;
    switch (type) {
      case "get":
        response = await axios.get(BASE_URL + request, {
          ...config,
          params: params,
        });
        break;
      case "post":
        response = await axios.post(BASE_URL + request, params, config);
        break;
      case "patch":
        response = await axios.patch(BASE_URL + request, params, config);
        break;
      case "put":
        response = await axios.put(BASE_URL + request, params, config);
        break;
      case "delete":
        response = await axios.delete(
          BASE_URL + request,
          {
            ...config,
            params: params,
          });
        break;
      default:
        throw new Error(`Unsupported request type: ${type}`);
    }

    console.log(`Success ${type} request!`, request);
    return response.data;
  } catch (error) {
    console.error("Ошибка при запросе:", error.message);
    return error.status;
  }
}

export async function get_cats(start = 0, end = 12, token) {
  const params = {
    skip: start,
    limit: end,
  };
  return req(params, "/cats", "get", token);
}

export async function search_cats(query, token) {
  const data = {
    query,
  };
  return req(data, "/search_cats", "post", token);
}

export async function register(first_name, last_name, phone_number, password) {
  const data = {
    first_name: first_name,
    last_name: last_name,
    phone_number: phone_number,
    password: password,
  };
  return req(data, "/register", "post", "");
}

export async function login(phone, password) {
  const data = {
    username: phone,
    password: password,
  };
  return req(data, "/login", "post");
}

export async function update_profile(
  first_name,
  last_name,
  phone_number,
  token
) {
  const data = {
    first_name: first_name,
    last_name: last_name,
    phone_number: phone_number,
  };
  return req(data, "/profile", "put", token);
}
export async function post_interview(
  question_1,
  question_2,
  question_3,
  question_4,
  question_5,
  question_6,
  question_7,
  question_8,
  question_9,
  question_10,
  token
) {
  const data = {
    answers: {
      question_1: question_1,
      question_2: question_2,
      question_3: question_3,
      question_4: question_4,
      question_5: question_5,
      question_6: question_6,
      question_7: question_7, // 1 - Да, 2 - Приют не имеет права, 3 - Нет
      question_8: question_8,
      question_9: question_9,
      question_10: question_10,
    },
  };
  return req(data, "/interview", "post", token);
}

export async function get_interview_status(token) {
  return req("", "/interview/status", "get", token);
}

export async function bind_cat(id, token) {
  const data = {
    cat_id: id,
  };
  return req(data, `/cats/${id}/book`, "post", token);
}

export async function get_book_cats(token) {
  return req("", `/admin/booked-cats`, "get", token);
}

export async function search_book_cats(name, token) {
  const data = {
    name: name,
  };
  return req(data, `/admin/search-booked-cats`, "post", token);
}

export async function unbind_cat(id, token) {
  const data = {
    cat_id: id,
  };
  return req(data, `/cats/${id}/unbook`, "post", token);
}

export async function get_favorite(token) {
  return req('', `/favorites`, "get", token);
}

export async function add_fav(id, token) {
  const data = {
    cat_id: id,
  };
  return req(data, `/cats/${id}/favorite`, "post", token);
}

export async function get_cat(id, token) {
  return req("", `/cats/${id}`, "get", token);
}

export async function send_priyut_form(formData, API_TOKEN) {
  const response = await axios.post(
          BASE_URL + '/shelter_application',
          formData,
          {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${API_TOKEN}`,
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        return response.data
}
