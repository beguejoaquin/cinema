"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { categories, movies } from "@/lib/placeholder-data";
import Link from "next/link";
import Image from "next/image";

export default function Home() {
  return (
    <>
      <h1 className="mx-auto my-5 text-4xl w-fit">CINEMA</h1>
      <div id="movies" className="w-3/4 mx-auto grid grid-cols-6 gap-2">
        {movies.map((movie) => (
          <Link href={`movie/${movie.id}/`} key={movie.id}>
            <Card key={movie.id}>
              <img
                src={movie.poster}
                width={300}
                height={600}
                className="relative z-20 w-full object-cover"
                key={movie.poster}
                alt="Movie Poster"
              />
              <CardHeader>
                <CardTitle>{movie.title}</CardTitle>
              </CardHeader>
            </Card>
          </Link>
        ))}
      </div>
    </>
  );
}
