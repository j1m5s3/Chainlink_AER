import React from "react";
import { List, Header, Rating, Divider } from "semantic-ui-react";

export const Movies = ({ movies }) => {
  return (
    <List>
      {movies.map(movie => {
        return (
          <List.Item key={movie.uuid}>
            <Header>City Name: {movie.data.city_name} |
            Field: {movie.data.field} |
            date: {movie.date} |
            uuid: {movie.uuid}</Header>
            <Divider horizontal>---------</Divider>
          </List.Item>
        );
      })}
    </List>
  );
};
