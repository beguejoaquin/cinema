export type Movie = {
  id: number;
  title: string;
  poster: string;
  duration: number;
  director: string;
  age_classification: string;
  synopsis: string;
  cast: [string];
  category: string;
};
export type Showtime = {
  id: number;
  movie_id: number;
  date: Date;
  theater: number;
  cinema: string;
};
