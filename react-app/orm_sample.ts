import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  try {
    // Get all students (equivalent to SELECT * FROM students)
    const students = await prisma.student.findMany();

    // Print each student
    for (const student of students) {
      console.log(student);
    }
  } catch (error) {
    console.error('Error fetching students:', error);
    throw error;
  } finally {
    // Disconnect Prisma client
    await prisma.$disconnect();
  }
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
