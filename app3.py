import streamlit as st
import json
import networkx as nx
from pyvis.network import Network
import tempfile
import os

# --------------------------------------------------
# STREAMLIT CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="NCERT Curriculum Knowledge Graph",
    layout="wide"
)

st.title("📘 NCERT Curriculum Knowledge Graph")
st.caption("Curriculum-aware knowledge graph for Grades 7–8 Science")

# --------------------------------------------------
# 🔴 PASTE YOUR FULL JSON HERE
# (Original JSON + Cross-Hub Bridges)
# --------------------------------------------------
INT_JSON = """
[
  {
    "source": "Force",
    "target": "Motion & Force",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Motion & Force",
      "context": "This concept is a fundamental building block within the Motion & Force module of the NCERT curriculum."
    }
  },
  {
    "source": "Motion",
    "target": "Motion & Force",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Motion & Force",
      "context": "This concept is a fundamental building block within the Motion & Force module of the NCERT curriculum."
    }
  },
  {
    "source": "Speed",
    "target": "Motion & Force",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Motion & Force",
      "context": "This concept is a fundamental building block within the Motion & Force module of the NCERT curriculum."
    }
  },
  {
    "source": "Acceleration",
    "target": "Motion & Force",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Motion & Force",
      "context": "This concept is a fundamental building block within the Motion & Force module of the NCERT curriculum."
    }
  },
  {
    "source": "Friction",
    "target": "Motion & Force",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Motion & Force",
      "context": "This concept is a fundamental building block within the Motion & Force module of the NCERT curriculum."
    }
  },
  {
    "source": "Gravity",
    "target": "Motion & Force",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Motion & Force",
      "context": "This concept is a fundamental building block within the Motion & Force module of the NCERT curriculum."
    }
  },
  {
    "source": "Light",
    "target": "Light & Sound",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Reflection",
    "target": "Light & Sound",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Refraction",
    "target": "Light & Sound",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Dispersion of Light",
    "target": "Light & Sound",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Sound",
    "target": "Light & Sound",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Vibration",
    "target": "Light & Sound",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Electric Current",
    "target": "Electricity & Magnetism",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Electric Circuit",
    "target": "Electricity & Magnetism",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Electric Cell",
    "target": "Electricity & Magnetism",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Magnet",
    "target": "Electricity & Magnetism",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Magnetic Poles",
    "target": "Electricity & Magnetism",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Electromagnet",
    "target": "Electricity & Magnetism",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Temperature",
    "target": "Heat",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Understanding temperature as a measure of hotness or coldness.",
      "context": "The concept of temperature from Grade 6 is fundamental to understanding the processes of heat transfer (conduction, convection, radiation) in Grade 7."
    }
  },
  {
    "source": "Conduction",
    "target": "Heat",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Heat",
      "context": "This concept is a fundamental building block within the Heat module of the NCERT curriculum."
    }
  },
  {
    "source": "Convection",
    "target": "Heat",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Heat",
      "context": "This concept is a fundamental building block within the Heat module of the NCERT curriculum."
    }
  },
  {
    "source": "Radiation",
    "target": "Heat",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Heat",
      "context": "This concept is a fundamental building block within the Heat module of the NCERT curriculum."
    }
  },
  {
    "source": "Matter",
    "target": "Matter & Materials",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Matter & Materials",
      "context": "This concept is a fundamental building block within the Matter & Materials module of the NCERT curriculum."
    }
  },
  {
    "source": "Physical Properties",
    "target": "Matter & Materials",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Matter & Materials",
      "context": "This concept is a fundamental building block within the Matter & Materials module of the NCERT curriculum."
    }
  },
  {
    "source": "States of Matter",
    "target": "Matter & Materials",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Matter & Materials",
      "context": "This concept is a fundamental building block within the Matter & Materials module of the NCERT curriculum."
    }
  },
  {
    "source": "Elements",
    "target": "Matter & Materials",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Matter & Materials",
      "context": "This concept is a fundamental building block within the Matter & Materials module of the NCERT curriculum."
    }
  },
  {
    "source": "Compounds",
    "target": "Matter & Materials",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Matter & Materials",
      "context": "This concept is a fundamental building block within the Matter & Materials module of the NCERT curriculum."
    }
  },
  {
    "source": "Mixtures",
    "target": "Matter & Materials",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Matter & Materials",
      "context": "This concept is a fundamental building block within the Matter & Materials module of the NCERT curriculum."
    }
  },
  {
    "source": "Chemical Reaction",
    "target": "Chemical Changes",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Chemical Changes",
      "context": "This concept is a fundamental building block within the Chemical Changes module of the NCERT curriculum."
    }
  },
  {
    "source": "Rusting",
    "target": "Chemical Changes",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Chemical Changes",
      "context": "This concept is a fundamental building block within the Chemical Changes module of the NCERT curriculum."
    }
  },
  {
    "source": "Burning",
    "target": "Chemical Changes",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Chemical Changes",
      "context": "This concept is a fundamental building block within the Chemical Changes module of the NCERT curriculum."
    }
  },
  {
    "source": "Oxidation",
    "target": "Chemical Changes",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Chemical Changes",
      "context": "This concept is a fundamental building block within the Chemical Changes module of the NCERT curriculum."
    }
  },
  {
    "source": "Reduction",
    "target": "Chemical Changes",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Chemical Changes",
      "context": "This concept is a fundamental building block within the Chemical Changes module of the NCERT curriculum."
    }
  },
  {
    "source": "Acids",
    "target": "Acids, Bases & Salts",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Acids, Bases & Salts",
      "context": "This concept is a fundamental building block within the Acids, Bases & Salts module of the NCERT curriculum."
    }
  },
  {
    "source": "Bases",
    "target": "Acids, Bases & Salts",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Acids, Bases & Salts",
      "context": "This concept is a fundamental building block within the Acids, Bases & Salts module of the NCERT curriculum."
    }
  },
  {
    "source": "Salts",
    "target": "Acids, Bases & Salts",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Acids, Bases & Salts",
      "context": "This concept is a fundamental building block within the Acids, Bases & Salts module of the NCERT curriculum."
    }
  },
  {
    "source": "Indicators",
    "target": "Acids, Bases & Salts",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Acids, Bases & Salts",
      "context": "This concept is a fundamental building block within the Acids, Bases & Salts module of the NCERT curriculum."
    }
  },
  {
    "source": "Neutralisation",
    "target": "Acids, Bases & Salts",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Acids, Bases & Salts",
      "context": "This concept is a fundamental building block within the Acids, Bases & Salts module of the NCERT curriculum."
    }
  },
  {
    "source": "Cell",
    "target": "Living Organisms",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Living Organisms",
      "context": "This concept is a fundamental building block within the Living Organisms module of the NCERT curriculum."
    }
  },
  {
    "source": "Tissue",
    "target": "Living Organisms",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Living Organisms",
      "context": "This concept is a fundamental building block within the Living Organisms module of the NCERT curriculum."
    }
  },
  {
    "source": "Microorganisms",
    "target": "Living Organisms",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Living Organisms",
      "context": "This concept is a fundamental building block within the Living Organisms module of the NCERT curriculum."
    }
  },
  {
    "source": "Nutrition",
    "target": "Food & Nutrition",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Food & Nutrition",
      "context": "This concept is a fundamental building block within the Food & Nutrition module of the NCERT curriculum."
    }
  },
  {
    "source": "Carbohydrates",
    "target": "Food & Nutrition",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Food & Nutrition",
      "context": "This concept is a fundamental building block within the Food & Nutrition module of the NCERT curriculum."
    }
  },
  {
    "source": "Proteins",
    "target": "Food & Nutrition",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Food & Nutrition",
      "context": "This concept is a fundamental building block within the Food & Nutrition module of the NCERT curriculum."
    }
  },
  {
    "source": "Fats",
    "target": "Food & Nutrition",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Food & Nutrition",
      "context": "This concept is a fundamental building block within the Food & Nutrition module of the NCERT curriculum."
    }
  },
  {
    "source": "Vitamins",
    "target": "Food & Nutrition",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Food & Nutrition",
      "context": "This concept is a fundamental building block within the Food & Nutrition module of the NCERT curriculum."
    }
  },
  {
    "source": "Digestive System",
    "target": "Human Body",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Human Body",
      "context": "This concept is a fundamental building block within the Human Body module of the NCERT curriculum."
    }
  },
  {
    "source": "Respiratory System",
    "target": "Human Body",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Human Body",
      "context": "This concept is a fundamental building block within the Human Body module of the NCERT curriculum."
    }
  },
  {
    "source": "Circulatory System",
    "target": "Human Body",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Human Body",
      "context": "This concept is a fundamental building block within the Human Body module of the NCERT curriculum."
    }
  },
  {
    "source": "Excretory System",
    "target": "Human Body",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Human Body",
      "context": "This concept is a fundamental building block within the Human Body module of the NCERT curriculum."
    }
  },
  {
    "source": "Photosynthesis",
    "target": "Plants",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Identifying the inputs (CO2, water, sunlight) and outputs (glucose, oxygen) of photosynthesis.",
      "context": "Grade 7 details the process of photosynthesis, building upon the Grade 6 concept that plants need food to grow."
    }
  },
  {
    "source": "Transpiration",
    "target": "Plants",
    "relation": "connects_to",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Plants",
      "context": "This concept is a fundamental building block within the Plants module of the NCERT curriculum."
    }
  },
  {
    "source": "Reproduction in Plants",
    "target": "Plants",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Plants",
      "context": "This concept is a fundamental building block within the Plants module of the NCERT curriculum."
    }
  },
  {
    "source": "Food Chain",
    "target": "Ecosystem",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Tracing the flow of energy from producers to consumers in an ecosystem.",
      "context": "A food chain is introduced as a simple linear pathway showing the feeding relationships and energy flow within an ecosystem."
    }
  },
  {
    "source": "Food Web",
    "target": "Ecosystem",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Ecosystem",
      "context": "This concept is a fundamental building block within the Ecosystem module of the NCERT curriculum."
    }
  },
  {
    "source": "Producers",
    "target": "Ecosystem",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Ecosystem",
      "context": "This concept is a fundamental building block within the Ecosystem module of the NCERT curriculum."
    }
  },
  {
    "source": "Consumers",
    "target": "Ecosystem",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Ecosystem",
      "context": "This concept is a fundamental building block within the Ecosystem module of the NCERT curriculum."
    }
  },
  {
    "source": "Decomposers",
    "target": "Ecosystem",
    "relation": "connects_to",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Ecosystem",
      "context": "This concept is a fundamental building block within the Ecosystem module of the NCERT curriculum."
    }
  },
  {
    "source": "Activity: Grouping plants based on height and stem",
    "target": "Classification of Plants",
    "relation": "demonstrated_by",
    "grade": "6",
    "metadata": {
      "learning_outcome": "Students learn to classify plants into herbs, shrubs, and trees by observing their physical characteristics.",
      "context": "Students perform a nature walk to observe and categorize plants into herbs, shrubs, and trees based on their stem and height."
    }
  },
  {
    "source": "Activity: Heating potassium permanganate in water",
    "target": "Convection",
    "relation": "demonstrated_by",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Visualizing the movement of particles in a liquid during heating.",
      "context": "Students observe colored streaks of potassium permanganate rising and falling in heated water, demonstrating heat transfer through fluid motion."
    }
  },
  {
    "source": "Activity: Deflection of a compass needle",
    "target": "Magnetic Effect of Electric Current",
    "relation": "demonstrated_by",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Observing that a current-carrying wire produces a magnetic field.",
      "context": "Students observe that a magnetic compass needle deflects when an electric current flows through a nearby wire, demonstrating the magnetic effect."
    }
  },
  {
    "source": "Activity: Water drop on an oiled surface",
    "target": "Lens",
    "relation": "demonstrated_by",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Observing the magnifying effect of a curved transparent surface.",
      "context": "Students observe that a drop of water on an oiled glass strip acts like a simple lens, magnifying the text placed underneath it."
    }
  },
  {
    "source": "Activity: Ball and stick model with a light source",
    "target": "Phases of the Moon",
    "relation": "demonstrated_by",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Simulating how the illuminated portion of the Moon visible from Earth changes as it revolves.",
      "context": "A student holding a ball (Moon) and turning around in front of a light source (Sun) simulates how different phases of the Moon are observed from Earth."
    }
  },
  {
    "source": "Activity: Observing onion peel under a microscope",
    "target": "Cell",
    "relation": "demonstrated_by",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Visualizing the basic structural unit of a plant.",
      "context": "Students prepare a slide of onion peel to observe the rectangular, brick-like arrangement of plant cells under a microscope."
    }
  },
  {
    "source": "Lifting Cranes",
    "target": "Electromagnet",
    "relation": "applied_in",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Understanding a large-scale industrial application of electromagnets.",
      "context": "The principle of the electromagnet is applied in large lifting cranes used in scrap yards to move heavy iron and steel objects."
    }
  },
  {
    "source": "Ant Bite Treatment",
    "target": "Neutralisation Reaction",
    "relation": "applied_in",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Applying the concept of acid-base neutralisation to a daily life problem.",
      "context": "The sting of an ant, which is acidic (formic acid), can be relieved by applying a basic substance like baking soda, demonstrating neutralisation."
    }
  },
  {
    "source": "Vehicle Side-view Mirrors",
    "target": "Convex Mirror",
    "relation": "applied_in",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Understanding the practical use of convex mirrors for a wider field of view.",
      "context": "Convex mirrors are used as side-view mirrors in vehicles because they provide a wider view of the road behind, even though they form diminished images."
    }
  },
  {
    "source": "Classification of Plants",
    "target": "Plants",
    "relation": "is_part_of",
    "grade": "6",
    "metadata": {
      "learning_outcome": "Core learning objective for Plants",
      "context": "This concept is a fundamental building block within the Plants module of the NCERT curriculum."
    }
  },
  {
    "source": "Magnetic Effect of Electric Current",
    "target": "Electricity & Magnetism",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Electricity & Magnetism",
      "context": "This concept is a fundamental building block within the Electricity & Magnetism module of the NCERT curriculum."
    }
  },
  {
    "source": "Lens",
    "target": "Light & Sound",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },
  {
    "source": "Neutralisation Reaction",
    "target": "Acids, Bases & Salts",
    "relation": "is_part_of",
    "grade": "7",
    "metadata": {
      "learning_outcome": "Core learning objective for Acids, Bases & Salts",
      "context": "This concept is a fundamental building block within the Acids, Bases & Salts module of the NCERT curriculum."
    }
  },
  {
    "source": "Convex Mirror",
    "target": "Light & Sound",
    "relation": "is_part_of",
    "grade": "8",
    "metadata": {
      "learning_outcome": "Core learning objective for Light & Sound",
      "context": "This concept is a fundamental building block within the Light & Sound module of the NCERT curriculum."
    }
  },

  { "source": "Friction", "target": "Heat", "relation": "causes", "grade": "7" },
  { "source": "Electric Current", "target": "Heating Effect", "relation": "causes", "grade": "7" },
  { "source": "Heating Effect", "target": "Heat", "relation": "related_to", "grade": "7" },

  { "source": "Photosynthesis", "target": "Food Chain", "relation": "prerequisite_for", "grade": "8" },
  { "source": "Photosynthesis", "target": "Producers", "relation": "related_to", "grade": "8" },

  { "source": "Food Chain", "target": "Energy", "relation": "related_to", "grade": "8" },
  { "source": "Energy", "target": "Motion", "relation": "related_to", "grade": "8" },

  { "source": "Respiratory System", "target": "Energy", "relation": "related_to", "grade": "7" },
  { "source": "Digestion", "target": "Energy", "relation": "related_to", "grade": "7" },

  { "source": "Microorganisms", "target": "Food Preservation", "relation": "applied_in", "grade": "8" },
  { "source": "Microorganisms", "target": "Decomposers", "relation": "related_to", "grade": "8" },

  { "source": "Oxidation", "target": "Rusting", "relation": "related_to", "grade": "8" },
  { "source": "Burning", "target": "Energy", "relation": "related_to", "grade": "7" },

  { "source": "Acids", "target": "Soil Quality", "relation": "related_to", "grade": "8" },
  { "source": "Soil Quality", "target": "Plants", "relation": "related_to", "grade": "8" },

  { "source": "Water Cycle", "target": "Ecosystem", "relation": "related_to", "grade": "8" },
  { "source": "Transpiration", "target": "Water Cycle", "relation": "related_to", "grade": "8" },

  { "source": "Light", "target": "Photosynthesis", "relation": "prerequisite_for", "grade": "7" },
  { "source": "Sound", "target": "Vibration", "relation": "related_to", "grade": "7" },

  { "source": "Cell", "target": "Tissue", "relation": "prerequisite_for", "grade": "8" },
  { "source": "Tissue", "target": "Human Body", "relation": "related_to", "grade": "8" },

  { "source": "Electricity", "target": "Energy", "relation": "related_to", "grade": "7" },
  { "source": "Magnet", "target": "Electric Current", "relation": "related_to", "grade": "8" }

]
"""
# --------------------------------------------------

# --------------------------------------------------
# LOAD JSON
# --------------------------------------------------
try:
    data = json.loads(INT_JSON)
except Exception as e:
    st.error("❌ Invalid JSON. Please check formatting.")
    st.stop()

# --------------------------------------------------
# FIXED CURRICULUM HUB ONTOLOGY
# --------------------------------------------------
TOPIC_HUBS = [
    "Motion & Force",
    "Light & Sound",
    "Electricity & Magnetism",
    "Heat",
    "Matter & Materials",
    "Chemical Changes",
    "Acids, Bases & Salts",
    "Living Organisms",
    "Food & Nutrition",
    "Human Body",
    "Plants",
    "Ecosystem"
]

# --------------------------------------------------
# EDGE COLOR SCHEMA (NEW)
# --------------------------------------------------
EDGE_COLORS = {
    "causes": "#e74c3c",           # red
    "prerequisite_for": "#8e44ad", # purple
    "applied_in": "#27ae60",       # green
    "related_to": "#95a5a6",       # grey
    "is_part_of": "#2980b9",       # blue
    "connects_to": "#7f8c8d"       # dark grey
}

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.header("🔍 Graph Controls")

selected_hub = st.sidebar.selectbox(
    "Focus on Topic Hub",
    ["All"] + TOPIC_HUBS
)

show_grade6 = st.sidebar.checkbox("Include Grade 6 Concepts", value=False)
show_activities = st.sidebar.checkbox("Show Activities", value=False)

# --------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------
G = nx.Graph()

# Add hub anchors first
for hub in TOPIC_HUBS:
    G.add_node(
        hub,
        node_type="hub",
        size=50,
        color="#f1c232"  # gold
    )

def classify_node(name):
    if name in TOPIC_HUBS:
        return "hub", "#f1c232", 50
    if name.startswith("Activity:"):
        return "activity", "#b7b7b7", 10
    return "concept", "#6fa8dc", 18

for item in data:
    src = item.get("source")
    tgt = item.get("target")
    relation = item.get("relation")
    grade = item.get("grade")

    if grade == "6" and not show_grade6:
        continue

    if src.startswith("Activity:") and not show_activities:
        continue

    src_type, src_color, src_size = classify_node(src)
    tgt_type, tgt_color, tgt_size = classify_node(tgt)

    if not G.has_node(src):
        G.add_node(src, node_type=src_type, color=src_color, size=src_size)

    if not G.has_node(tgt):
        G.add_node(tgt, node_type=tgt_type, color=tgt_color, size=tgt_size)

    G.add_edge(src, tgt, label=relation)

# --------------------------------------------------
# FILTER BY HUB
# --------------------------------------------------
if selected_hub != "All":
    connected_nodes = nx.node_connected_component(G, selected_hub)
    G = G.subgraph(connected_nodes).copy()

# --------------------------------------------------
# RENDER GRAPH (WITH COLORED EDGES)
# --------------------------------------------------
net = Network(
    height="750px",
    width="100%",
    bgcolor="#ffffff",
    font_color="#000000"
)

for node, attrs in G.nodes(data=True):
    net.add_node(
        node,
        label=node,
        size=attrs.get("size", 15),
        color=attrs.get("color", "#cccccc")
    )

for u, v, attrs in G.edges(data=True):
    relation = attrs.get("label", "")
    net.add_edge(
        u,
        v,
        title=relation,
        color=EDGE_COLORS.get(relation, "#cccccc")
    )

net.repulsion(
    node_distance=180,
    central_gravity=0.2,
    spring_length=200,
    spring_strength=0.05,
    damping=0.9
)

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
    net.save_graph(tmp.name)
    html_path = tmp.name

st.components.v1.html(open(html_path).read(), height=750)
os.remove(html_path)

# --------------------------------------------------
# EXPLANATION PANEL
# --------------------------------------------------
st.markdown("### 🧠 How to read this graph")
st.markdown("""
- **Gold nodes** → Curriculum Topic Hubs  
- **Blue nodes** → Scientific concepts  
- **Grey nodes** → Activities  
- **Red edges** → Causality  
- **Purple edges** → Learning prerequisites  
- **Green edges** → Real-world applications  
- **Grey edges** → Conceptual relationships  

This graph represents **curriculum logic**, not textbook order.
""")

st.markdown("---")
st.markdown("Built using Google AI Studio + Streamlit")
