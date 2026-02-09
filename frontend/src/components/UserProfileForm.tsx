import React, { useState } from "react";
import type { UserProfile } from "../types";

interface UserProfileFormProps {
  onSubmit: (profile: UserProfile) => void;
  isLoading?: boolean; // Controls the loading state of the submit button
}

const FITNESS_LEVELS = ["Beginner", "Intermediate", "Advanced"];
const GOAL_OPTIONS = [
  "Weight Loss",
  "Muscle Gain",
  "Endurance",
  "Flexibility",
  "General Health",
  "Strength",
];
const EQUIPMENT_OPTIONS = [
  "Full Gym",
  "Dumbbells",
  "Resistance Bands",
  "Kettlebells",
  "Pull-up Bar",
  "Treadmill",
  "Bodyweight Only",
];

const UserProfileForm: React.FC<UserProfileFormProps> = ({
  onSubmit,
  isLoading = false,
}) => {
  const [fitnessLevel, setFitnessLevel] = useState<string>("Beginner");
  const [selectedGoals, setSelectedGoals] = useState<string[]>([]);
  const [selectedEquipment, setSelectedEquipment] = useState<string[]>([]);
  const [limitations, setLimitations] = useState<string>("");

  const handleGoalChange = (goal: string) => {
    setSelectedGoals((prev) =>
      prev.includes(goal) ? prev.filter((g) => g !== goal) : [...prev, goal],
    );
  };

  const handleEquipmentChange = (item: string) => {
    setSelectedEquipment((prev) =>
      prev.includes(item) ? prev.filter((e) => e !== item) : [...prev, item],
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Convert limitations string to array if present
    const limitationsArray = limitations
      .split(",")
      .map((l) => l.trim())
      .filter((l) => l.length > 0);

    const profile: UserProfile = {
      fitness_level: fitnessLevel as "Beginner" | "Intermediate" | "Advanced",
      goals: selectedGoals,
      equipment: selectedEquipment,
      limitations: limitationsArray,
    };

    onSubmit(profile);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6 bg-white p-6 rounded-lg shadow-md"
    >
      <div>
        <h2 className="text-xl font-bold mb-4 text-gray-800">
          Your Fitness Profile
        </h2>
        <p className="text-sm text-gray-500 mb-6">
          Tell us about yourself so we can generate the perfect plan.
        </p>
      </div>

      {/* Fitness Level */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Fitness Level
        </label>
        <div className="flex space-x-4">
          {FITNESS_LEVELS.map((level) => (
            <label
              key={level}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="radio"
                name="fitnessLevel"
                value={level}
                checked={fitnessLevel === level}
                onChange={(e) => setFitnessLevel(e.target.value)}
                className="form-radio h-4 w-4 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-gray-700">{level}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Goals */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Goals (Select all that apply)
        </label>
        <div className="grid grid-cols-2 gap-2">
          {GOAL_OPTIONS.map((goal) => (
            <label
              key={goal}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                value={goal}
                checked={selectedGoals.includes(goal)}
                onChange={() => handleGoalChange(goal)}
                className="form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
              />
              <span className="text-gray-700">{goal}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Equipment */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Available Equipment
        </label>
        <div className="grid grid-cols-2 gap-2">
          {EQUIPMENT_OPTIONS.map((item) => (
            <label
              key={item}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                value={item}
                checked={selectedEquipment.includes(item)}
                onChange={() => handleEquipmentChange(item)}
                className="form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
              />
              <span className="text-gray-700">{item}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Limitations */}
      <div>
        <label
          htmlFor="limitations"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Limitations / Injuries (Optional)
        </label>
        <input
          type="text"
          id="limitations"
          value={limitations}
          onChange={(e) => setLimitations(e.target.value)}
          placeholder="e.g., knee pain, low back injury (comma separated)"
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || selectedGoals.length === 0}
        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
          isLoading || selectedGoals.length === 0
            ? "bg-blue-300 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        }`}
      >
        {isLoading ? (
          <span className="flex items-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Generating Plan...
          </span>
        ) : (
          "Generate Weekly Plan"
        )}
      </button>
    </form>
  );
};

export default UserProfileForm;
