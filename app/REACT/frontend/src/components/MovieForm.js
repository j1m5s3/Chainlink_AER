import React, { useState } from "react";
import { Form, Input, Rating, Button } from "semantic-ui-react";

export const MovieForm = ({ onNewMovie }) => {
  const [city_name, setCityName] = useState("");
  const [field, setField] = useState("");
  const [request, setRequest] = useState({});

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="City Name"
          value={city_name}
          onChange={e => setCityName(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Input
          placeholder="field"
          value={field}
          onChange={e => setField(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        <Button
          onClick={async () => {
            const movie = { city_name, field };
            const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(movie)
            }

            const response = await fetch("/create_request",requestOptions);
            const data = await response.json();
            console.log(data);

            if (response.ok) {
              console.log("response worked!");
              onNewMovie(data.request);
              setCityName("");
              setField("");
            }
          }}
        >
          submit
        </Button>
      </Form.Field>
    </Form>
  );
};
