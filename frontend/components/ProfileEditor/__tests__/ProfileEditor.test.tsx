/**
 * @jest-environment jsdom
 */

import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";

import { ProfileEditor } from "../ProfileEditor";


it("renders correctly", () => {
  render(<ProfileEditor />);
  expect(screen.getByText("Profiles")).toBeInTheDocument();
});
