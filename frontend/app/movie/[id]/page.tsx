"use client";

import Image from "next/image";
import { movies, showtimes } from "@/lib/placeholder-data";
import { Movie, Showtime } from "@/lib/definitions";
import React, { useState, useMemo, useEffect } from "react";

export default function Page({ params }: { params: Promise<{ id: string }> }) {
  // Get movie details
  const { id } = React.use(params);
  const movie = movies.find((movie) => movie.id === parseInt(id));

  // Create the days to select a showtime
  const days = useMemo(() => {
    const daysArray = [];
    const today = new Date();
    for (let index = 0; index < 5; index++) {
      const day = new Date();
      day.setDate(today.getDate() + index);
      daysArray.push(day);
    }
    return daysArray;
  }, []);

  // Fetch showtimes for selected day
  const [selectedDay, useSelectedDay] = useState("");
  const [availableShowtimes, useAvailableShowtimes] = useState(Array<Showtime>);

  // Set initial value after days are computed
  useEffect(() => {
    if (days.length > 0 && !selectedDay) {
      useSelectedDay(days[0].toISOString());
    }
  }, [days, selectedDay]);

  const fetchShowtimes = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = new Date(event.target.value);
    useSelectedDay(event.target.value);
    useAvailableShowtimes(
      showtimes.filter(
        (showtime) =>
          showtime.date.getFullYear() === selectedValue.getFullYear() &&
          showtime.date.getMonth() === selectedValue.getMonth() &&
          showtime.date.getDate() === selectedValue.getDate(),
      ),
    );
    console.log(availableShowtimes);
  };

  const [selectedShowtime, useSelectedShowtime] = useState("");
  const updateSelectedShowtime = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    useSelectedShowtime(event.target.value);
  };

  return (
    <>
      <div id="movie-details">
        <h3>{movie?.title}</h3>
        <img src={movie?.poster || "default_poster.jpg"} alt="Movie Poster" />
      </div>
      <div id="showtimes">
        <select
          name="date"
          id="date"
          value={selectedDay}
          onChange={fetchShowtimes}
        >
          {days.map((day, index) => (
            <option key={index} value={day.toISOString()}>
              {day.toLocaleDateString("en-US", { weekday: "long" })}{" "}
              {day.getDate()}
            </option>
          ))}
        </select>
        <select
          name="showtime"
          id="showtime"
          value={selectedShowtime}
          onChange={updateSelectedShowtime}
        >
          {availableShowtimes.map((showtime, index) => (
            <option key={index} value={showtime.date.toISOString()}>
              {showtime.date.toLocaleTimeString()}
            </option>
          ))}
        </select>
      </div>
    </>
  );
}
